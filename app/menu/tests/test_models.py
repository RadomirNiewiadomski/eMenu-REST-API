"""
Tests for models.
"""
from decimal import Decimal

from unittest.mock import patch

from django.test import TestCase

from menu.models import Menu, Dish, dish_image_file_path


class ModelTest(TestCase):
    """Test models."""
    def test_create_menu(self):
        """Test creating a menu is successful."""
        menu = Menu.objects.create(
            title='Some cuisine',
        )

        self.assertEqual(str(menu), menu.title)

    def test_create_dish(self):
        """Test creating a dish is successful."""
        dish = Dish.objects.create(
            title='Some cuisine',
            description='Some description',
            time_minutes='15',
            price=Decimal('2.50'),
            vegetarian=False,
        )

        self.assertEqual(str(dish), dish.title)

    @patch('menu.models.uuid.uuid4')
    def test_dish_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = dish_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/dish/{uuid}.jpg')
