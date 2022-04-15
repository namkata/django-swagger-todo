from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from account.serializers import MyTokenObtainPairSerializer
from account.serializers import MyTokenRefreshSerializer
from account.serializers import MyTokenVerifySerializer
from drf_yasg.utils import swagger_auto_schema


class MyTokenObtainPairView(TokenObtainPairView, ObtainAuthToken):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        responses={
            200: MyTokenObtainPairSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

    @swagger_auto_schema(
        responses={
            200: MyTokenRefreshSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MyTokenVerifyView(TokenVerifyView):
    serializer_class = MyTokenVerifySerializer

    @swagger_auto_schema(
        responses={
            200: MyTokenVerifySerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
