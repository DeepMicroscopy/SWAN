import csv

from django.db.models import OuterRef, Subquery
from django.http.response import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action

from app import util
from app.models import ClassificationUser, ClassificationAnonymous


def get_data_users(study):
    latest = ClassificationUser.objects.filter(
        user=OuterRef("user"),
        study=OuterRef("study"),
        index=OuterRef("index")
    ).order_by("-date").values("pk")[:1]

    result = []

    for entry in ClassificationUser.objects.filter(study_id=study, id__in=Subquery(latest)):
        result.append(
            [int(entry.date.timestamp()), entry.study.id, entry.file, entry.choice, entry.user.id]
        )

    return result


def get_data_anonymous(study):
    latest = ClassificationAnonymous.objects.filter(
        session=OuterRef("session"),
        study=OuterRef("study"),
        index=OuterRef("index")
    ).order_by("-date").values("pk")[:1]

    result = []

    for entry in ClassificationAnonymous.objects.filter(study_id=study, id__in=Subquery(latest)):
        result.append(
            [int(entry.date.timestamp()), entry.study.id, entry.file, entry.choice, entry.session]
        )

    return result


def get_data(study):
    users = get_data_users(study)
    anonymous = get_data_anonymous(study)

    users.extend(anonymous)

    return users


@extend_schema(tags=['Export'], parameters=[OpenApiParameter("study", OpenApiTypes.UUID, OpenApiParameter.PATH)])
class ExportViewSet(viewsets.ViewSet):
    lookup_url_kwarg = "study"

    @extend_schema(
        responses=OpenApiTypes.STR,
        description="A QR code linking to this study",
    )
    @action(detail=True, renderer_classes=[util.SVGRenderer])
    def csv(self, request, study=None):
        response = HttpResponse(content_type="text/plain")

        writer = csv.writer(response)

        writer.writerow(["time", "study", "file", "choice", "user_or_session"])
        writer.writerows(get_data(study))

        return response
