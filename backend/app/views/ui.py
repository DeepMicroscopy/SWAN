from drf_spectacular.utils import extend_schema
from rest_framework import mixins, serializers, viewsets
from rest_framework.permissions import IsAdminUser

from app.models import Ui
from app.views.study import UiLabelSerializer


class UiAdminSerializer(serializers.ModelSerializer):
    labels = UiLabelSerializer()

    class Meta:
        model = Ui
        fields = ["id", "title", "labels"]


@extend_schema(tags=['Ui'])
class UiViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """The swipe interface (labels per direction) that studies are shown with."""
    queryset = Ui.objects.order_by("title")
    serializer_class = UiAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None
