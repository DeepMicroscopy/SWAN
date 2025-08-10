import datetime

from app import util
from app.models import Study
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ClassificationUser, ClassificationAnonymous


class ClassifyInputSerializer(serializers.Serializer):
    study = serializers.UUIDField(required=True)
    choice = serializers.IntegerField(required=True)
    index = serializers.IntegerField(required=True)


class ClassifyOutputSerializer(serializers.Serializer):
    study = serializers.UUIDField(required=True, source="study_id")
    choice = serializers.IntegerField(required=True)
    index = serializers.IntegerField(required=True)


@extend_schema(tags=['Classify'])
class ClassifyViewSet(viewsets.ViewSet):
    @extend_schema(
        request=ClassifyInputSerializer,
        responses=ClassifyOutputSerializer,
    )
    def create(self, request):
        serializer = ClassifyInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        queryset = Study.objects.filter(group__in=util.groups(request)).select_related("dataset")
        study = get_object_or_404(queryset, pk=data["study"])

        if data["index"] >= study.dataset.file_count:
            return HttpResponse("index too large", status=400)

        items = util.deterministic_shuffle(
            study.dataset.file_list,
            util.seed_from(request.user, request.session, data["study"])
        )
        file = items[data["index"]]

        if request.user.username == "anonymous":
            result, created = ClassificationAnonymous.objects.create(
                date=datetime.datetime.now(),
                session=request.session.session_key,
                study_id=data["study"], file=file, choice=data["choice"], index=data["index"]
            )
        else:
            result = ClassificationUser.objects.create(
                date=datetime.datetime.now(),
                user=request.user,
                study_id=data["study"], file=file, choice=data["choice"], index=data["index"]
            )

        serializer = ClassifyOutputSerializer(result)
        return Response(serializer.data)
