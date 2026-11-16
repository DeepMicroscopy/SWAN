from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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


class GroupCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    usernames = serializers.ListField(child=serializers.CharField(), required=False, default=list,
                                      help_text="Members of the group; every one must be an existing user.")


@extend_schema(tags=['Group'])
class GroupViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Reviewer groups. A study with a group is only visible to its members.

    `POST` makes a group with the given members, or - when a group of that name exists - adds the members to it (it never
    removes anyone and never touches other groups), so a service can set groups up repeatedly."""
    queryset = Group.objects.order_by("name").prefetch_related("user_set")
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None

    @extend_schema(request=GroupCreateSerializer, responses=GroupSerializer)
    def create(self, request, *args, **kwargs):
        data = GroupCreateSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        names = list(dict.fromkeys(data.validated_data["usernames"]))
        users = list(User.objects.filter(username__in=names))
        missing = sorted(set(names) - {u.username for u in users})
        if missing:
            return Response({"usernames": [f"no such user: {', '.join(missing)}"]}, status=status.HTTP_400_BAD_REQUEST)
        group, created = Group.objects.get_or_create(name=data.validated_data["name"])
        for u in users:
            u.groups.add(group)
        group = Group.objects.prefetch_related("user_set").get(pk=group.pk)
        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
