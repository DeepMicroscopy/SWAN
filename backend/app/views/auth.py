from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class StatusSerializer(serializers.Serializer):
    authenticated = serializers.BooleanField()
    username = serializers.CharField()


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


@extend_schema(tags=['Auth'])
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(request=None, responses=StatusSerializer)
    @action(detail=False, methods=['get'])
    def status(self, request):
        serializer = StatusSerializer({
            "authenticated": request.user.is_authenticated,
            "username": request.user.username if request.user.is_authenticated else None
        })

        response = Response(serializer.data)
        ensure_csrf_cookie(lambda r: response)(request._request)
        return response

    @extend_schema(request=LoginSerializer, responses=DetailSerializer)
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

    @extend_schema(request=None, responses=DetailSerializer)
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)

        return Response({"detail": "Logged out successfully"})
