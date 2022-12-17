"""
URL mappings for the user API.
"""
from django.urls import path

from . import views

app_name = 'user' # reversed mapping

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
