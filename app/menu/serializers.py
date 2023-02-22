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

    def _get_or_create_dishes(self, dishes, menu):
        """Handle getting or creating dishes as needed."""
        for dish in dishes:
            dish_obj, created = Dish.objects.get_or_create(**dish)
            menu.dishes.add(dish_obj)

    def create(self, validated_data):
        """Create a menu."""
        dishes = validated_data.pop('dishes', [])
        menu = Menu.objects.create(**validated_data)
        self._get_or_create_dishes(dishes, menu)

        return menu

    def update(self, instance, validated_data):
        """Update a menu."""
        dishes = validated_data.pop('dishes', None)
        if dishes is not None:
            instance.dishes.clear()
            self._get_or_create_dishes(dishes, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MenuDetailSerializer(MenuSerializer):
    """Serializer for menu detail view."""
    dishes = DishSerializer(many=True, required=False)

    class Meta(MenuSerializer.Meta):
        fields = MenuSerializer.Meta.fields + ['description', 'dishes']
