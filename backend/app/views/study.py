import datetime
import os

import magic
from django.contrib.auth.models import Group
from django.db.models import Count, Max, Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app import util
from app.models import Study, ClassificationAnonymous, ClassificationUser, Dataset, Ui, Solution
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
    length = serializers.IntegerField(source="dataset.file_count")
    index = serializers.SerializerMethodField()

    @staticmethod
    def get_educational(study: Study) -> bool:
        return hasattr(study, "solution")

    def get_index(self, study: Study) -> int:
        request = self.context.get("request")
        return get_index_for_request(request, study.id)

    class Meta:
        model = Study
        fields = ["id", "title", "description", "image", "pub_date", "end_date", "educational", "length", "index"]

class StudySerializer(StudyListSerializer):
    solution = SolutionConfigSerializer(allow_null=True)
    ui = UiSerializer()

    class Meta(StudyListSerializer.Meta):
        fields = StudyListSerializer.Meta.fields + ["solution", "ui"]

class PostponedSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.IntegerField())


class StudyCreateSerializer(serializers.ModelSerializer):
    dataset = serializers.PrimaryKeyRelatedField(queryset=Dataset.objects.all())
    ui = serializers.PrimaryKeyRelatedField(queryset=Ui.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Study
        fields = ["id", "title", "description", "pub_date", "end_date", "group", "anonymous", "dataset", "ui"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["end_date"] <= attrs["pub_date"]:
            raise serializers.ValidationError("end_date must be after pub_date")
        return attrs


class ReviewerProgressSerializer(serializers.Serializer):
    user = serializers.UUIDField(allow_null=True)
    username = serializers.CharField()
    classified = serializers.IntegerField()
    complete = serializers.BooleanField()
    last_activity = serializers.DateTimeField(allow_null=True)


class StudyProgressSerializer(serializers.Serializer):
    study = serializers.UUIDField()
    file_count = serializers.IntegerField()
    reviewers = ReviewerProgressSerializer(many=True)
    complete_reviewers = serializers.IntegerField()


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

    @extend_schema(request=StudyCreateSerializer, responses=StudyCreateSerializer)
    def create(self, request):
        serializer = StudyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        study = serializer.save()
        return Response(StudyCreateSerializer(study).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=None, responses=StudyProgressSerializer)
    @action(detail=True, methods=["get"])
    def progress(self, request, pk=None):
        """How many images each reviewer has classified. A reviewer is complete once every image has an answer.

        Members of the study's group are listed even if they have not started yet."""
        study = get_object_or_404(Study.objects.select_related("dataset", "group"), pk=pk)
        file_count = study.dataset.file_count or 0

        rows = (
            ClassificationUser.objects.filter(study=study)
            .values("user", "user__username")
            .annotate(classified=Count("index", distinct=True), last_activity=Max("date"))
        )
        reviewers = {
            row["user"]: {
                "user": row["user"], "username": row["user__username"] or "(deleted user)",
                "classified": row["classified"], "last_activity": row["last_activity"],
            }
            for row in rows
        }
        if study.group is not None:
            for member in study.group.user_set.all():
                reviewers.setdefault(member.id, {
                    "user": member.id, "username": member.username, "classified": 0, "last_activity": None,
                })

        result = sorted(reviewers.values(), key=lambda r: r["username"])
        for r in result:
            r["complete"] = file_count > 0 and r["classified"] >= file_count

        serializer = StudyProgressSerializer({
            "study": study.id,
            "file_count": file_count,
            "reviewers": result,
            "complete_reviewers": sum(1 for r in result if r["complete"]),
        })
        return Response(serializer.data)
