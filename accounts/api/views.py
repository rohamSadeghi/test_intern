from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase

from accounts.api.serializers import TokenLifetimeSerializer, RefreshLifetimeSerializer, RegisterSerializer, \
    SetPasswordSerializer
from accounts.models import User
from utils.throttles import PhoneNumberScopedRateThrottle


class ObtainTokenView(TokenViewBase):
    serializer_class = TokenLifetimeSerializer


class RefreshTokenView(TokenViewBase):
    serializer_class = RefreshLifetimeSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    throttle_classes = [PhoneNumberScopedRateThrottle, ]
    throttle_scope = 'register'


class SetPasswordView(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("New password set successfully", status=status.HTTP_201_CREATED)

