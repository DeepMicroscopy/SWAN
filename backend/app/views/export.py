import csv

import itertools
from django.db.models import OuterRef, Subquery, F
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

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

    queryset = Study.objects.all()
    ui = get_object_or_404(queryset, pk=study).ui

    def label(choice):
        if choice in ui.labels:
            if "label" in ui.labels[choice]:
                return ui.labels[choice]["label"]
            elif "text" in ui.labels[choice]:
                return ui.labels[choice]["text"]

        return None

    def change(entry):
        entry["time"] = entry["date"].timestamp()
        entry["label"] = label(entry["choice"])
        del entry["date"]
        return entry

    return list(map(change, itertools.chain(users, anonymous)))


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
        response = HttpResponse(content_type="text/plain")
        writer = csv.DictWriter(response, fieldnames=FIELD_NAMES)

        writer.writeheader()
        writer.writerows(get_data(study))

        return response
