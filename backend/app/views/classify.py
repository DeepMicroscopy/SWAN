import base64
import uuid

import magic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from app import util
from app.models import ClassificationUser, ClassificationAnonymous, Classification, Study
from app.views.util import study_queryset_for_request, session_for_request


class ClassifyInputSerializer(serializers.Serializer):
    study = serializers.UUIDField(required=True)
    choice = serializers.ChoiceField(required=True, choices=("up", "down", "left", "right"))
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
    def get_queryset(self):
        if self.action == "create":
            return ClassificationUser.objects.all()
        elif self.action == "view":
            return Study.objects.all()
        else:
            raise Exception()

    def get_permissions(self):
        if self.action == "create" or self.action == "view":
            return [AllowAny()]
        else:
            return [IsAdminUser()]

    @extend_schema(
        request=None,
        responses=ClassifyOutputSerializer,
    )
    @action(detail=True, url_path='(?P<index>[0-9]+)')
    def view(self, request, pk=None, index=None):
        if request.user.is_anonymous and not util.check_tag(str(pk), request.COOKIES.get("anonymous")):
            return Response({"detail": "invalid authentication tag"}, status=status.HTTP_403_FORBIDDEN)

        queryset = study_queryset_for_request(request)
        study = get_object_or_404(queryset, pk=pk)

        if request.user.is_authenticated:
            result = ClassificationUser.objects.filter(user=request.user, study=study, index=index)
        else:
            result = ClassificationAnonymous.objects.filter(session=session_for_request(request), study=study, index=index)

        ordered = result.order_by("-date")
        if ordered.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ClassifyOutputSerializer(ordered.first())
        return Response(serializer.data)

    @extend_schema(
        request=ClassifyInputSerializer,
        responses=ClassifyOutputSerializer,
    )
    def create(self, request):
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
            util.seed_from(request.user, session_for_request(request), data["study"])
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
                session=session_for_request(request),
                study_id=data["study"], file=file, choice=data["choice"], index=data["index"]
            )

        serializer = ClassifyOutputSerializer(result)
        return Response(serializer.data)
