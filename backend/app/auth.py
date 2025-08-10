from django.contrib.auth import authenticate, login, logout

from drf_spectacular.utils import extend_schema

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


@extend_schema(tags=['Auth'])
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        return Response({"detail": "Logged in successfully"})

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)

        return Response({"detail": "Logged out successfully"})
