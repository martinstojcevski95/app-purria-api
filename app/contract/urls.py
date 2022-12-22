"""
URL mappings for the contract app.
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from contract import views

router = DefaultRouter()
router.register('contracts', views.ContractViewSet)
router.register('gardens', views.GardenViewSet)

app_name = 'contract'

urlpatterns = [
    path('', include(router.urls)),
]
