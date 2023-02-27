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

from menu.tests.creates import (
    create_dish,
    create_menu
)


MENU_URL = reverse('menu:menu-list')


def detail_url(menu_id):
    """Create and return a menu detail URL."""
    return reverse('menu:menu-detail', args=[menu_id])


class PublicMenuApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_menus_list(self):
        """Test retrieving a list of not empty menus - public."""
        m1 = create_menu(title='Some cuisine 1')
        m2 = create_menu(title='Some cuisine 2')
        m3 = create_menu(title='Some cuisine 3')
        dish = create_dish()
        m1.dishes.add(dish)
        m2.dishes.add(dish)

        res = self.client.get(MENU_URL)

        s1 = MenuSerializer(m1)
        s2 = MenuSerializer(m2)
        s3 = MenuSerializer(m3)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

    def test_get_menu_detail(self):
        """Test get menu detail - public."""
        menu = create_menu()

        url = detail_url(menu.id)
        res = self.client.get(url)

        serializer = MenuDetailSerializer(menu)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required(self):
        """Test auth is required (for POST method)."""
        payload = {
            'title': 'Sample menu',
            'description': "Sample description"
        }
        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMenuApiTests(TestCase):
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
        menu = Menu.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(menu, k), v)

    def test_partial_update(self):
        """Test partial update of a menu - private."""
        original_description = 'Sample menu title'
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
            title='Sample menu title',
            description='Sample menu description',
        )
        payload = {
            'title': 'New menu title',
            'description': 'New menu description',
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

    def test_create_menu_with_new_dishes(self):
        """Test creating menu with new dishes - private."""
        payload = {
            'title': 'Menu card 1',
            'dishes': [
                {
                    'title': 'Some dish1',
                    'price': Decimal('5.00'),
                    'time_minutes': 30,
                    'vegetarian': False,
                },
                {
                    'title': 'Some dish2',
                    'price': Decimal('7.00'),
                    'time_minutes': 20,
                    'vegetarian': True,
                }]
        }
        res = self.client.post(MENU_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        menus = Menu.objects.all()
        self.assertEqual(menus.count(), 1)
        menu = menus[0]
        self.assertEqual(menu.dishes.count(), 2)
        for dish in payload['dishes']:
            exists = menu.dishes.filter(
                title=dish['title'],
                price=dish['price'],
                time_minutes=dish['time_minutes'],
                vegetarian=dish['vegetarian'],
            ).exists()
            self.assertTrue(exists)

    def test_create_menu_with_existing_dish(self):
        """Test creating menu with existing dish - private."""
        dish_meatballs = create_dish(
            title='Meatballs',
            price=Decimal('6.50'),
            time_minutes=30,
            vegetarian=False
        )
        payload = {
            'title': 'Menu card 1',
            'dishes': [
                {
                    'title': 'Meatballs',
                    'price': Decimal('6.50'),
                    'time_minutes': 30,
                    'vegetarian': False,
                },
                {
                    'title': 'Some dish2',
                    'price': Decimal('7.00'),
                    'time_minutes': 20,
                    'vegetarian': True,
                }]
        }
        res = self.client.post(MENU_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        menus = Menu.objects.all()
        self.assertEqual(menus.count(), 1)
        menu = menus[0]
        self.assertEqual(menu.dishes.count(), 2)
        self.assertIn(dish_meatballs, menu.dishes.all())
        for dish in payload['dishes']:
            exists = menu.dishes.filter(
                title=dish['title'],
                price=dish['price'],
                time_minutes=dish['time_minutes'],
                vegetarian=dish['vegetarian'],
            ).exists()
            self.assertTrue(exists)

    def test_create_dish_on_update(self):
        """Test creating dish when updating a menu - private."""
        menu = create_menu()

        payload = {'dishes': [{
            'title': 'Some dish1',
            'price': Decimal('5.00'),
            'time_minutes': 30,
            'vegetarian': False,
        }]}
        url = detail_url(menu.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_dish = Dish.objects.get(title='Some dish1')
        self.assertIn(new_dish, menu.dishes.all())

    def test_update_menu_assign_dish(self):
        """Test assigning an existing dish when updating a menu - private."""
        dish_meatballs = create_dish(
            title='Meatballs',
            price=Decimal('6.50'),
            time_minutes=30,
            vegetarian=False
        )
        menu = create_menu()
        menu.dishes.add(dish_meatballs)

        dish_spaghetti = create_dish(
            title='Spaghetti',
            price=Decimal('8.00'),
            time_minutes=40,
            vegetarian=False
        )
        payload = {'dishes': [{'title': 'Spaghetti', 'price': Decimal(
            '8.00'), 'time_minutes': 40, 'vegetarian': False}]}
        url = detail_url(menu.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(dish_spaghetti, menu.dishes.all())
        self.assertNotIn(dish_meatballs, menu.dishes.all())

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
