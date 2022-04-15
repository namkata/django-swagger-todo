from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.serializers import RefreshToken

from account.models import MyToken, used_timedelta, MyUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = authenticate(
            username=attrs['username'],
            password=attrs['password'])
        if not user.refresh_token:
            refresh = self.get_token(user)
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
            user.refresh_token = str(refresh)
            user.save()
            MyToken.objects.create(user=user, key=str(refresh.access_token))
        else:
            data['refresh'] = user.refresh_token
            if MyToken.objects.filter(user=user).first():
                MyToken.objects.get(user=user).delete()
            key = str(RefreshToken(user.refresh_token).access_token)
            MyToken.objects.create(user=user, key=key)
            data['access'] = key

        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        user = MyUser.objects.get(refresh_token=refresh)
        MyToken.objects.filter(user=user).update(
            key=str(refresh.access_token),
            used_time=used_timedelta())
        data = {"access": str(refresh.access_token),
                "refresh": str(refresh)}
        return data


class MyTokenVerifySerializer(TokenVerifySerializer):
    token_class = RefreshToken
