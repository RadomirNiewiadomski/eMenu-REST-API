"""
Test for the dishes API.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Dish

from menu.serializers import DishSerializer

DISHES_URL = reverse('menu:dish-list')


def detail_url(dish_id):
    """Create and return a dish detail URL."""
    return reverse('menu:dish-detail', args=[dish_id])


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


class PublicDishApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_dishes_list(self):
        """Test retrieving a list of dishes - public."""
        create_dish()
        create_dish(
            title='Meatballs',
            price=Decimal('6.50'),
            time_minutes=30,
            vegetarian=False
        )

        res = self.client.get(DISHES_URL)

        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_dish_detail(self):
        """Test get dish detail - public."""
        dish = create_dish()

        url = detail_url(dish.id)
        res = self.client.get(url)

        serializer = DishSerializer(dish)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required(self):
        """Test auth is required (for POST method)."""
        payload = {
            'title': 'Some dish1',
            'price': Decimal('5.00'),
            'time_minutes': 30,
            'vegetarian': False,
        }
        res = self.client.post(DISHES_URL, payload)

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

    def test_create_dish(self):
        """Test creating a dish - private."""
        payload = {
            'title': 'Some dish1',
            'price': Decimal('5.00'),
            'time_minutes': 30,
            'vegetarian': False,
        }
        res = self.client.post(DISHES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        dish = Dish.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(dish, k), v)

    def test_update_dish(self):
        """Test updating a dish - private."""
        dish = create_dish(
            title='Meatballs',
            price=Decimal('6.50'),
            time_minutes=30,
            vegetarian=False
        )

        payload = {
            'title': 'Some dish1',
            'price': Decimal('5.00'),
            'time_minutes': 30,
            'vegetarian': False,
        }
        url = detail_url(dish.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        dish.refresh_from_db()
        self.assertEqual(dish.title, payload['title'])

    def test_delete_dish(self):
        """Test deleting a dish."""
        dish = create_dish(
            title='Meatballs',
            price=Decimal('6.50'),
            time_minutes=30,
            vegetarian=False
        )

        url = detail_url(dish.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Dish.objects.all().exists())
