"""
Serializers for menu API.
"""
from rest_framework import serializers

from core.models import (
    Menu,
    Dish,
)


class DishSerializer(serializers.ModelSerializer):
    """Serializer for dish."""

    class Meta():
        model = Dish
        fields = '__all__'
        read_only_fields = ['id']


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for menu."""

    class Meta:
        model = Menu
        fields = ['id', 'title']
        read_only_fields = ['id']


class MenuDetailSerializer(MenuSerializer):
    """Serializer for menu detail view."""

    class Meta(MenuSerializer.Meta):
        fields = MenuSerializer.Meta.fields + ['description', 'dishes']
