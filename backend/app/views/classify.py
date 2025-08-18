import base64
import uuid

import magic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from app import util
from app.models import ClassificationUser, ClassificationAnonymous, Classification
from app.views.util import study_queryset_for_request


class ClassifyInputSerializer(serializers.Serializer):
    study = serializers.UUIDField(required=True)
    choice = serializers.CharField(required=True)
    index = serializers.IntegerField(required=True)


class SolutionSerializer(serializers.Serializer):
    text = serializers.CharField()


class EducationSerializer(serializers.Serializer):
    solution = SolutionSerializer()
    proof = serializers.CharField(allow_null=True)


class ClassifyOutputSerializer(serializers.Serializer):
    study = serializers.UUIDField(source="study_id")
    choice = serializers.CharField()
    index = serializers.IntegerField()
    education = serializers.SerializerMethodField(allow_null=True)

    @staticmethod
    def get_education(obj: Classification) -> EducationSerializer:
        if not hasattr(obj.study, "solution"):
            return None

        solution = obj.study.solution

        if obj.file not in solution.config:
            solution.config[obj.file] = {"text": ""}
            solution.save(update_fields=["config"])

        try:
            file_data = util.extract_file_data(solution.archive, obj.file)
            mime_type = magic.from_buffer(file_data, mime=True)
            proof = f"data:{mime_type};base64,{base64.b64encode(file_data).decode()}"
        except KeyError:
            proof = None

        serializer = EducationSerializer({
            "solution": solution.config[obj.file],
            "proof": proof
        })
        return serializer.data


@extend_schema(tags=['Classify'])
class ClassifyViewSet(viewsets.ViewSet):
    queryset = ClassificationUser.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    @extend_schema(
        request=ClassifyInputSerializer,
        responses=ClassifyOutputSerializer,
    )
    def create(self, request):
        # should have been set by requesting an entry, so error out here
        if not request.session.session_key:
            return Response({"detail":"expected a session"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ClassifyInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        study_id: uuid.UUID = data["study"]

        if request.user.is_anonymous and not util.check_tag(str(study_id), request.COOKIES.get("anonymous")):
            return Response({"detail": "invalid authentication tag"}, status=status.HTTP_403_FORBIDDEN)

        queryset = study_queryset_for_request(request)
        study = get_object_or_404(queryset.select_related("dataset"), pk=study_id)

        if data["index"] >= study.dataset.file_count:
            return HttpResponse("index too large", status=400)

        items = util.deterministic_shuffle(
            study.dataset.file_list,
            util.seed_from(request.user, request.session.session_key, data["study"])
        )
        file = items[data["index"]]

        if request.user.is_authenticated:
            result = ClassificationUser.objects.create(
                date=timezone.now(),
                user=request.user,
                study_id=data["study"], file=file, choice=data["choice"], index=data["index"]
            )
        else:
            result = ClassificationAnonymous.objects.create(
                date=timezone.now(),
                session=request.session.session_key,
                study_id=data["study"], file=file, choice=data["choice"], index=data["index"]
            )

        serializer = ClassifyOutputSerializer(result)
        return Response(serializer.data)
