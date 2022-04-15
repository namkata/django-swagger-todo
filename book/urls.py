from django.urls import path
from book import views

urlpatterns = [
    path('books', views.BookAPI.as_view(), name='api-books'),
]
