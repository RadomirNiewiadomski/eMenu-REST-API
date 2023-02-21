"""
Views for the menu API.
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import (
    Menu,
    Dish,
)
from menu import serializers


class MenuViewSet(viewsets.ModelViewSet):
    """View for manage menu APIs."""
    serializer_class = serializers.MenuDetailSerializer
    queryset = Menu.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve list of menus."""

        return self.queryset.all().order_by('-id')

    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == 'list':
            return serializers.MenuSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new menu."""
        serializer.save()


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DishSerializer
    queryset = Dish.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve list of dishes."""

        return self.queryset.all().order_by('-id')

    def perform_create(self, serializer):
        """Create a new dish."""
        serializer.save()
