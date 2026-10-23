import csv

import itertools
from django.db.models import OuterRef, Subquery, F
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from app import util
from app.models import ClassificationUser, ClassificationAnonymous, Study

FIELD_NAMES = ["time", "study", "file", "choice", "label", "user_or_session"]
TABLE_NAMES = ["date"] + FIELD_NAMES.copy()
TABLE_NAMES.remove("time")
TABLE_NAMES.remove("label")


def get_queryset_users(study):
    latest = ClassificationUser.objects.filter(
        user=OuterRef("user"),
        study=OuterRef("study"),
        index=OuterRef("index")
    ).order_by("-date").values("pk")[:1]

    return ClassificationUser.objects.filter(study_id=study, id__in=Subquery(latest))


def get_queryset_anonymous(study):
    latest = ClassificationAnonymous.objects.filter(
        session=OuterRef("session"),
        study=OuterRef("study"),
        index=OuterRef("index")
    ).order_by("-date").values("pk")[:1]

    return ClassificationAnonymous.objects.filter(study_id=study, id__in=Subquery(latest))


def get_data(study):
    users = get_queryset_users(study).annotate(
        user_or_session=F("user"),
    ).values(*TABLE_NAMES)

    anonymous = get_queryset_anonymous(study).annotate(
        user_or_session=F("session"),
    ).values(*TABLE_NAMES)

    return itertools.chain(users, anonymous)


@extend_schema(tags=['Export'], parameters=[OpenApiParameter("study", OpenApiTypes.UUID, OpenApiParameter.PATH)])
class ExportViewSet(viewsets.ViewSet):
    lookup_url_kwarg = "study"
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses=OpenApiTypes.STR,
        description="A QR code linking to this study",
    )
    @action(detail=True, renderer_classes=[util.SVGRenderer])
    def csv(self, request, study=None):
        queryset = Study.objects.all()
        ui = get_object_or_404(queryset, pk=study).ui

        writer = csv.DictWriter(ExportViewSet.Util.Echo(), fieldnames=FIELD_NAMES)

        def generator():
            yield writer.writeheader()

            for row in get_data(study):
                yield writer.writerow(ExportViewSet.Util.change(row, ui))

        return StreamingHttpResponse(generator(), content_type="text/plain")

    @extend_schema(
        responses=OpenApiTypes.OBJECT,
        description="The latest classification of every registered reviewer for each image, as JSON",
    )
    @action(detail=True)
    def results(self, request, study=None):
        study_obj = get_object_or_404(Study.objects.select_related("ui", "dataset"), pk=study)
        ui = study_obj.ui

        rows = get_queryset_users(study).order_by("file", "user__username").values(
            "date", "file", "choice", "index", "user", "user__username",
        )
        return Response({
            "study": str(study_obj.id),
            "file_count": study_obj.dataset.file_count,
            "classifications": [
                {
                    "file": row["file"],
                    "choice": row["choice"],
                    "label": ExportViewSet.Util.label(row["choice"], ui),
                    "user": str(row["user"]) if row["user"] else None,
                    "username": row["user__username"],
                    "date": row["date"],
                }
                for row in rows
            ],
        })

    class Util:
        @staticmethod
        def label(choice, ui):
            if choice in ui.labels:
                if "label" in ui.labels[choice]:
                    return ui.labels[choice]["label"]
                elif "text" in ui.labels[choice]:
                    return ui.labels[choice]["text"]

            return None

        @staticmethod
        def change(entry, ui):
            entry["time"] = entry["date"].timestamp()
            entry["label"] = ExportViewSet.Util.label(entry["choice"], ui)
            del entry["date"]
            return entry

        class Echo:
            @staticmethod
            def write(value):
                return value
