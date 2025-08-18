import datetime
import os

import magic
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app import util
from app.models import Study, ClassificationAnonymous, ClassificationUser, Ui
from swan import settings


def get_index_for_request(request, pk):
    if request.user.username == "anonymous":
        result = ClassificationAnonymous.objects.filter(
            study=pk,
            session=request.session.session_key,
            study__group__in=util.groups(request)
        ).order_by("-index").first()
    else:
        result = ClassificationUser.objects.filter(
            study=pk,
            user=request.user,
            study__group__in=util.groups(request)
        ).order_by("-index").first()

    if result is None:
        return 0
    else:
        return result.index

class UiSerializer(serializers.HyperlinkedModelSerializer):
    class UiLabelSerializer(serializers.Serializer):
        left = serializers.DictField()
        right = serializers.DictField()
        up = serializers.DictField(required=False)
        down = serializers.DictField(required=False)

    labels = UiLabelSerializer()

    class Meta:
        model = Ui
        fields = ["title", "labels"]

class StudySerializer(serializers.HyperlinkedModelSerializer):
    ui = UiSerializer()
    length = serializers.IntegerField(source="dataset.file_count")
    index = serializers.SerializerMethodField()

    def get_index(self, study: Study) -> int:
        request = self.context.get("request")
        return get_index_for_request(request, study.id)

    class Meta:
        model = Study
        fields = ["id", "title", "description", "image", "pub_date", "end_date", "ui", "length", "index"]

class StudyListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "title", "description", "image", "pub_date", "end_date"]

@extend_schema(tags=['Study'])
class StudyViewSet(viewsets.GenericViewSet):
    queryset = Study.objects.all()

    def get_serializer(self, context):
        if self.action == "list":
            return StudyListSerializer
        else:
            return StudySerializer

    def list(self, request):
        now = datetime.datetime.now(datetime.timezone.utc)
        queryset = Study.objects.filter(
            pub_date__lte=now, end_date__gt=now, group__in=util.groups(request)
        )
        serializer = StudyListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Study.objects.filter(group__in=util.groups(request))
        study = get_object_or_404(queryset, pk=pk)
        serializer = StudySerializer(study, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        operation_id="v1_studies_retrieve_entry",
        responses=OpenApiTypes.BINARY,
        description="The file at the index of the dataset based on the user"
    )
    @action(detail=True, url_path="(?P<index>[0-9]+)", renderer_classes=[util.FileRenderer])
    def entry(self, request, pk=None, index=None):
        index = int(index)
        queryset = Study.objects.filter(group__in=util.groups(request)).select_related("dataset")
        study = get_object_or_404(queryset, pk=pk)

        if index >= study.dataset.file_count:
            return Response(status=status.HTTP_204_NO_CONTENT)

        items = util.deterministic_shuffle(study.dataset.file_list, util.seed_from(request.user, request.session, pk))
        file_data = util.extract_file_data(os.path.join(settings.MEDIA_ROOT, study.dataset.archive.path), items[index])

        return HttpResponse(file_data, content_type=magic.from_buffer(file_data, mime=True))
