from django.urls import path
from . import views

urlpatterns = [
    path('sign-in', views.MyTokenObtainPairView.as_view(), name='sign-in'),
    path('renew-token',
         views.MyTokenRefreshView.as_view(),
         name='renew-token'),
    path('verify', views.MyTokenVerifyView.as_view(), name='verify'),
]
