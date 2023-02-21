"""
Tests for menu API.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Menu,
    Dish,
)

from menu.serializers import (
    MenuSerializer,
    MenuDetailSerializer,
)


MENU_URL = reverse('menu:menu-list')


def detail_url(menu_id):
    """Create and return a menu detail URL."""
    return reverse('menu:menu-detail', args=[menu_id])


def create_menu(**params):
    """Create and return a sample menu."""
    defaults = {
        'title': 'Some cuisine',
    }
    defaults.update(params)

    menu = Menu.objects.create(**defaults)
    return menu


def create_dish(**params):
    """Create and return a sample dish."""
    defaults = {
        'title': 'Some dish',
        'price': Decimal('5.00'),
        'time_minutes': 30,
        'vegetarian': False,
    }
    defaults.update(params)

    dish = Dish.objects.create(**defaults)
    return dish


class PublicMenuApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_menus_list(self):
        """Test retrieving a list of menus - public."""
        create_menu()
        create_menu(title='Some cuisine 2')

        res = self.client.get(MENU_URL)

        menus = Menu.objects.all().order_by('-id')
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_menu_detail(self):
        """Test get menu detail - public."""
        menu = create_menu()

        url = detail_url(menu.id)
        res = self.client.get(url)

        serializer = MenuDetailSerializer(menu)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required(self):
        """Test auth is required for POST method."""
        payload = {
            'title': 'Sample menu',
            'description': "Sample description"
        }
        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_menu(self):
        """Test creating a menu - private."""
        payload = {
            'title': 'Sample menu',
            'description': "Sample description"
        }
        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Menu.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_partial_update(self):
        """Test partial update of a menu - private."""
        original_description = 'Sample recipe title'
        menu = create_menu(
            title='Old menu title',
            description=original_description,
        )

        payload = {'title': 'New menu title'}
        url = detail_url(menu.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        menu.refresh_from_db()
        self.assertEqual(menu.title, payload['title'])
        self.assertEqual(menu.description, original_description)

    def test_full_update(self):
        """Test full update of a menu - private."""
        menu = create_menu(
            title='Sample recipe title',
            description='Sample recipe description',
        )
        payload = {
            'title': 'New recipe title',
            'description': 'New recipe description',
        }
        url = detail_url(menu.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        menu.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(menu, k), v)

    def test_delete_menu(self):
        """Test deleting a menu successful - private."""
        menu = create_menu()

        url = detail_url(menu.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=menu.id).exists())

    def test_clear_dishes_from_menu(self):
        """Test clearing dishes from menu - private."""
        dish = create_dish()
        menu = create_menu()
        menu.dishes.add(dish)

        payload = {'dishes': []}
        url = detail_url(menu.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(menu.dishes.count(), 0)
