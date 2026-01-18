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
from app.models import Study, ClassificationAnonymous, ClassificationUser, Ui, Solution
from app.views.export import get_queryset_users, get_queryset_anonymous
from app.views.util import study_queryset_for_request, session_for_request
from swan import settings


def get_index_for_request(request, study):
    if request.user.is_authenticated:
        result = ClassificationUser.objects.filter(
            study=study,
            user=request.user,
        ).order_by("-index").first()
    else:
        result = ClassificationAnonymous.objects.filter(
            study=study,
            session=session_for_request(request),
        ).order_by("-index").first()

    if result is None:
        return 0
    else:
        return result.index + 1


def get_postponed_for_request(request, study, direction):
    if request.user.is_authenticated:
        queryset = get_queryset_users(study).filter(user=request.user)
    else:
        queryset = get_queryset_anonymous(study).filter(session=session_for_request(request))

    queryset = queryset.filter(choice=direction)

    return queryset.order_by("index").values_list("index", flat=True)


class UiDirectionSerializer(serializers.Serializer):
    text = serializers.CharField(allow_null=True)
    color = serializers.CharField(allow_null=True)
    icon = serializers.CharField(allow_null=True)


class UiLabelSerializer(serializers.Serializer):
    left = UiDirectionSerializer(allow_null=True)
    right = UiDirectionSerializer(allow_null=True)
    up = UiDirectionSerializer(allow_null=True)
    down = UiDirectionSerializer(allow_null=True)


class UiSerializer(serializers.HyperlinkedModelSerializer):
    labels = UiLabelSerializer()

    class Meta:
        model = Ui
        fields = ["title", "labels", "postpone", "pixelated", "default_scale"]


class SolutionConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Solution
        fields = ["label_current", "label_proof", "css_row", "css_column"]


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
    solution = SolutionConfigSerializer(allow_null=True)

    def get_index(self, study: Study) -> int:
        request = self.context.get("request")
        return get_index_for_request(request, study.id)

    class Meta:
        model = Study
        fields = ["id", "title", "description", "image", "pub_date", "end_date", "solution", "ui", "length", "index"]


class PostponedSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.IntegerField())


@extend_schema(tags=['Study'])
class StudyViewSet(viewsets.GenericViewSet):
    queryset = Study.objects.all()

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "entry" or self.action == "postponed":
            return [AllowAny()]
        elif self.action == "list":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_serializer(self, context):
        if self.action == "postponed":
            return PostponedSerializer
        elif self.action == "list":
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

        serializer = StudyListSerializer(queryset, many=True, context={"request": request})
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
        if request.user.is_anonymous and not util.check_tag(pk, request.COOKIES.get("anonymous")):
            return Response({"detail": "invalid authentication tag"}, status=status.HTTP_403_FORBIDDEN)

        queryset = study_queryset_for_request(request)
        study = get_object_or_404(queryset.select_related("dataset"), pk=pk)

        index = int(index)
        if index >= study.dataset.file_count:
            return Response(status=status.HTTP_204_NO_CONTENT)

        items = util.deterministic_shuffle(
            study.dataset.file_list,
            util.seed_from(request.user, session_for_request(request), pk)
        )
        file_data = util.extract_file_data(os.path.join(settings.MEDIA_ROOT, study.dataset.archive.path), items[index])

        return HttpResponse(file_data, content_type=magic.from_buffer(file_data, mime=True))

    @action(detail=True)
    def postponed(self, request, pk=None):
        if request.user.is_anonymous and not util.check_tag(pk, request.COOKIES.get("anonymous")):
            return Response({"detail": "invalid authentication tag"}, status=status.HTTP_403_FORBIDDEN)

        queryset = study_queryset_for_request(request)
        ui = get_object_or_404(queryset, pk=pk).ui

        if ui.postpone is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = PostponedSerializer({"images": get_postponed_for_request(request, pk, ui.postpone)})
        return Response(serializer.data)
