import random

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class TokenLifetimeSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['expire'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class RefreshLifetimeSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['expire'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number',]

    def create(self, validated_data):
        phone_number = validated_data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)

        if settings.DEVEL:
            verify_code = 22222
        else:
            # TODO: Add send sms function here
            verify_code = random.randint(10000, 99999)

        user.set_verify_code(verify_code)
        return user


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(_("new password and confirm password did not match"))
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['request'].user

        if user.has_usable_password():
            raise serializers.ValidationError(_("This user has already set password before"))
        user.set_password(validated_data['confirm_password'])
        user.save()
        return user
