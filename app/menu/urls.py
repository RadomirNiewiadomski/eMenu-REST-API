"""
URL mappings for the menu app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from menu import views


router = DefaultRouter()
router.register('menu', views.MenuViewSet)
router.register('dish', views.DishViewSet)

app_name = 'menu'

urlpatterns = [
    path('', include(router.urls)),
]
