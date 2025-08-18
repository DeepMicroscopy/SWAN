from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from app import util
from app.models import Study


@extend_schema(tags=['Share'], parameters=[OpenApiParameter("study", OpenApiTypes.UUID, OpenApiParameter.PATH)])
class ShareViewSet(viewsets.ViewSet):
    lookup_url_kwarg = "study"
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses=OpenApiTypes.STR,
        description="A link to this study",
    )
    @action(detail=True, renderer_classes=[util.SVGRenderer])
    def link(self, request, study=None):
        obj: Study = get_object_or_404(Study.objects.all(), pk=study)

        if obj.anonymous:
            return HttpResponse(request.build_absolute_uri(f"/#/studies/{study}/{util.create_tag(study)}"))
        else:
            return HttpResponse(request.build_absolute_uri(f"/#/studies/{study}"))

    @extend_schema(
        responses=OpenApiTypes.STR,
        description="A QR code linking to this study",
    )
    @action(detail=True, renderer_classes=[util.SVGRenderer])
    def users(self, request, study=None):
        return HttpResponse(
            util.create_qr(request.build_absolute_uri(f"/#/studies/{study}")),
            content_type="image/svg+xml"
        )

    @extend_schema(
        responses=OpenApiTypes.STR,
        description="A QR code linking to this study with an authorization for anonymous access",
    )
    @action(detail=True, renderer_classes=[util.SVGRenderer])
    def anonymous(self, request, study: str = None):
        return HttpResponse(
            util.create_qr(request.build_absolute_uri(f"/#/studies/{study}/{util.create_tag(study)}")),
            content_type="image/svg+xml"
        )
