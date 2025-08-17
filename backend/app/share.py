from django.http.response import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action

from . import util


@extend_schema(
    tags=['Share'],
    parameters=[
        OpenApiParameter(
            name="study", type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH, required=True,
            description="Primary key"
        ),
    ],
)
class ShareViewSet(viewsets.ViewSet):
    lookup_url_kwarg = "study"

    # TODO
    #  - add anonymous with token
    @extend_schema(
        responses=OpenApiTypes.STR,
        description="A QR code linking to this study",
    )
    @action(detail=True, renderer_classes=[util.SVGRenderer])
    def users(self, request, pk=None):
        return HttpResponse(util.create_qr(request.build_absolute_uri(f"/#/studies/{pk}")), content_type="image/svg+xml")
