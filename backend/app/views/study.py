import datetime
import os

import magic
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app import util
from app.models import Study, ClassificationAnonymous, ClassificationUser, Ui
from app.views.util import study_queryset_for_request
from swan import settings


def get_index_for_request(request, pk):
    if request.user.is_authenticated:
        result = ClassificationUser.objects.filter(
            study=pk,
            user=request.user,
            study__group__in=util.groups(request)
        ).order_by("-index").first()
    else:
        result = ClassificationAnonymous.objects.filter(
            study=pk,
            session=request.session.session_key,
            study__group__in=util.groups(request)
        ).order_by("-index").first()

    if result is None:
        return 0
    else:
        return result.index


class UiDirectionSerializer(serializers.Serializer):
    text = serializers.CharField()
    color = serializers.CharField(allow_null=True)
    icon = serializers.CharField(allow_null=True)


class UiLabelSerializer(serializers.Serializer):
    left = UiDirectionSerializer()
    right = UiDirectionSerializer()
    up = UiDirectionSerializer(allow_null=True)
    down = UiDirectionSerializer(allow_null=True)


class UiSerializer(serializers.HyperlinkedModelSerializer):
    labels = UiLabelSerializer()

    class Meta:
        model = Ui
        fields = ["title", "labels"]

class StudyListSerializer(serializers.HyperlinkedModelSerializer):
    educational = serializers.SerializerMethodField()

    @staticmethod
    def get_educational(study: Study) -> bool:
        return hasattr(study, "solution")

    class Meta:
        model = Study
        fields = ["id", "title", "description", "image", "pub_date", "end_date", "educational"]

class StudySerializer(StudyListSerializer):
    ui = UiSerializer()
    length = serializers.IntegerField(source="dataset.file_count")
    index = serializers.SerializerMethodField()

    def get_index(self, study: Study) -> int:
        request = self.context.get("request")
        return get_index_for_request(request, study.id)

    class Meta:
        model = Study
        fields = ["id", "title", "description", "image", "pub_date", "end_date", "educational", "ui", "length", "index"]

@extend_schema(tags=['Study'])
class StudyViewSet(viewsets.GenericViewSet):
    queryset = Study.objects.all()

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "entry":
            return [AllowAny()]
        elif self.action == "list":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_serializer(self, context):
        if self.action == "list":
            return StudyListSerializer
        else:
            return StudySerializer

    @staticmethod
    def list(request):
        now = datetime.datetime.now(datetime.timezone.utc)
        queryset = Study.objects.filter(
            Q(pub_date__lte=now, end_date__gt=now) & (
                    Q(group__in=util.groups(request))
                    | Q(group__isnull=True)
                    | Q(anonymous=True)
            )
        )

        serializer = StudyListSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk=None):
        if request.user.is_anonymous and not util.check_tag(pk, request.COOKIES.get("anonymous")):
            return Response({"detail": "invalid authentication tag"}, status=status.HTTP_403_FORBIDDEN)

        queryset = study_queryset_for_request(request)
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
        # ensure session exists for deterministic_shuffle
        if not request.session.session_key:
            request.session.create()

        if request.user.is_anonymous and not util.check_tag(pk, request.COOKIES.get("anonymous")):
            return Response({"detail": "invalid authentication tag"}, status=status.HTTP_403_FORBIDDEN)

        queryset = study_queryset_for_request(request)
        study = get_object_or_404(queryset.select_related("dataset"), pk=pk)

        index = int(index)
        if index >= study.dataset.file_count:
            return Response(status=status.HTTP_204_NO_CONTENT)

        items = util.deterministic_shuffle(
            study.dataset.file_list,
            util.seed_from(request.user, request.session.session_key, pk)
        )
        file_data = util.extract_file_data(os.path.join(settings.MEDIA_ROOT, study.dataset.archive.path), items[index])

        return HttpResponse(file_data, content_type=magic.from_buffer(file_data, mime=True))
