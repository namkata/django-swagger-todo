from django.urls import path
from book import views

urlpatterns = [
    path('books', views.books, name='api-books'),
]
