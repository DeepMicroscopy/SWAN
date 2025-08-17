import datetime
import os

import magic
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from swan import settings
from . import util
from .models import Study, ClassificationAnonymous, ClassificationUser


class StudySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "title", "image", "pub_date", "end_date", "ui"]


@extend_schema(
    tags=['Study'],
    parameters=[
        OpenApiParameter(
            name="id", type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH, required=True,
            description="Primary key"
        ),
    ],
)
class StudyViewSet(viewsets.GenericViewSet):
    serializer_class = StudySerializer

    def list(self, request, *args, **kwargs):
        now = datetime.datetime.now(datetime.timezone.utc)
        queryset = Study.objects.filter(
            pub_date__lte=now, end_date__gt=now, group__in=util.groups(request)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Study.objects.filter(group__in=util.groups(request))
        study = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(study)
        return Response(serializer.data)

    @extend_schema(
        responses=OpenApiTypes.INT,
        description="The current index in the dataset for this study based on the user"
    )
    @action(detail=True)
    def index(self, request, pk=None):
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
            return Response(0)
        else:
            return Response(result.index)

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
