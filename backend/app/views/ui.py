from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAdminUser

from app.models import Ui


class UiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ui
        fields = ["id", "title"]


@extend_schema(tags=['Ui'])
class UiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ui.objects.all()
    serializer_class = UiSerializer
    permission_classes = [IsAdminUser]
