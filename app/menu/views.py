"""
Views for the menu API.
"""
from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter

from .filters import MenuFilter
from menu.models import Menu, Dish
from menu import serializers


class MenuViewSet(viewsets.ModelViewSet):
    """View for manage menu APIs."""

    serializer_class = serializers.MenuDetailSerializer
    queryset = Menu.objects.all().annotate(dish_count=Count('dishes'))
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MenuFilter
    ordering_fields = ['title', 'dish_count']

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(dishes__isnull=False).distinct()

        return self.queryset

    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == 'list':
            return serializers.MenuSerializer

        return self.serializer_class


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DishSerializer
    queryset = Dish.objects.all().order_by('title')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == 'upload_image':
            return serializers.DishImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a dish."""
        dish = self.get_object()
        serializer = self.get_serializer(dish, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
