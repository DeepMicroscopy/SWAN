from app import util
from django.http.response import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action


@extend_schema(tags=['Share'])
class ShareViewSet(viewsets.ViewSet):
    lookup_url_kwarg = "study"

    # TODO
    #  - add anonymous with token
    @extend_schema(
        responses=OpenApiTypes.STR,
        description="A QR code linking to this study",
        parameters=[OpenApiParameter("study", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    )
    @action(detail=True, renderer_classes=[util.SVGRenderer])
    def users(self, request, study=None):
        return HttpResponse(
            util.create_qr(request.build_absolute_uri(f"/#/studies/{study}")),
            content_type="image/svg+xml"
        )
