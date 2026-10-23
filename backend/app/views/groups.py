from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAdminUser

from app.models import User


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class GroupSerializer(serializers.ModelSerializer):
    user_set = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "user_set"]


@extend_schema(tags=['Group'])
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Reviewer groups. A study with a group is only visible to its members."""
    queryset = Group.objects.order_by("name").prefetch_related("user_set")
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None
