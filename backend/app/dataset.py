import os
import magic

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter

from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from swan import settings
from . import util
from .models import Dataset


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "title", "archive", "file_count", "file_list"]


@extend_schema(
    tags=['Dataset'],
    parameters=[
        OpenApiParameter(
            name="id", type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH, required=True,
            description="Primary key"
        ),
    ],
)
class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="v1_datasets_retrieve_entry",
        responses=OpenApiTypes.BINARY,
        description="The file at the index of the dataset",
    )
    @action(detail=True, url_path="(?P<index>\d+)", renderer_classes=[util.FileRenderer])
    def entry(self, request, pk=None, index: int = None):
        index = int(index)
        queryset = Dataset.objects.all()
        dataset = get_object_or_404(queryset, pk=pk)

        if index >= dataset.file_count:
            return Response(status=status.HTTP_204_NO_CONTENT)

        file_data = util.extract_file_data(os.path.join(settings.MEDIA_ROOT, dataset.archive.path),
                                           dataset.file_list[index])

        return HttpResponse(file_data, content_type=magic.from_buffer(file_data, mime=True))
