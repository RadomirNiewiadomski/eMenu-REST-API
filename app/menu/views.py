"""
Views for the menu API.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Menu, Dish

from menu import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'title',
                OpenApiTypes.STR,
                description='Filter menus by title',
            ),
            OpenApiParameter(
                'created_date',
                OpenApiTypes.DATE,
                description='Filter menus created from date',
            ),
            OpenApiParameter(
                'modified_date',
                OpenApiTypes.DATE,
                description='Filter menus modified from date',
            ),
        ]
    )
)
class MenuViewSet(viewsets.ModelViewSet):
    """View for manage menu APIs."""
    serializer_class = serializers.MenuDetailSerializer
    queryset = Menu.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            dishes = Dish.objects.all()
            self.queryset = Menu.objects.filter(dishes__in=dishes).distinct()
            title = self.request.query_params.get('title')
            created_date = self.request.query_params.get('created_date')
            modified_date = self.request.query_params.get('modified_date')
            if title:
                self.queryset = self.queryset.filter(title=title)
            if created_date:
                self.queryset = self.queryset.filter(
                    created_date__gte=created_date)
            if modified_date:
                self.queryset = self.queryset.filter(
                    modified_date__gte=modified_date)

        return self.queryset.distinct()

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
