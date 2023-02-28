from rest_framework.test import APIClient

from django.urls import reverse
from django.utils.timezone import now, timedelta


from rest_framework.test import APITestCase

from menu.serializers import MenuSerializer

from menu.tests.creates import (
    create_dish,
    create_menu
)

MENU_URL = reverse('menu:menu-list')


class MenuApiFilterTests(APITestCase):
    """Test filtering and sorting menus."""

    def setUp(self):
        self.client = APIClient()
        self.menu1 = create_menu(title='Monday menu')
        self.dish1 = create_dish(title='Burger')
        self.menu1.dishes.add(self.dish1)
        self.s1 = MenuSerializer(self.menu1)

        self.menu2 = create_menu(title='Tuesday menu')
        self.dish2 = create_dish(title='Pizza')
        self.menu2.dishes.add(self.dish2)
        self.s2 = MenuSerializer(self.menu2)

        self.menu3 = create_menu(title='Wednesday menu')
        self.dish3 = create_dish(title='Egg salad')
        self.dish4 = create_dish(title='Tomato soup')
        self.dish5 = create_dish(title='Margherita')
        self.menu3.dishes.add(self.dish3, self.dish4, self.dish5)
        self.s3 = MenuSerializer(self.menu3)

        self.menu4 = create_menu(title='Thursday menu')
        self.s4 = MenuSerializer(self.menu4)

        self.yesterday = (now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.today = now().strftime('%Y-%m-%d')
        self.tomorrow = (now() + timedelta(days=1)).strftime('%Y-%m-%d')

    def test_get_filtered_menus_by_name(self):
        """Test filtering menus by name."""
        url = MENU_URL

        params = {'title': 'menu'}
        res = self.client.get(url, params)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.s1.data, res.data)
        self.assertIn(self.s2.data, res.data)
        self.assertIn(self.s3.data, res.data)
        self.assertNotIn(self.s4.data, res.data)
        self.assertEqual(len(res.data), 3)

        params = {'title': 'royal'}
        res = self.client.get(url, params)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(self.s1.data, res.data)
        self.assertNotIn(self.s2.data, res.data)
        self.assertNotIn(self.s3.data, res.data)
        self.assertNotIn(self.s4.data, res.data)
        self.assertEqual(len(res.data), 0)

        params = {'title': 'Monday'}
        res = self.client.get(url, params)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.s1.data, res.data)
        self.assertNotIn(self.s2.data, res.data)
        self.assertNotIn(self.s3.data, res.data)
        self.assertNotIn(self.s4.data, res.data)
        self.assertEqual(len(res.data), 1)

    def test_get_filtered_menus_bY_created_and_modified_date(self):
        """Test filtering menus by created and modified date."""
        url = MENU_URL

        params = {'created_from': self.today, 'created_to': self.tomorrow}
        res = self.client.get(url, params)
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.s1.data, res.data)
        self.assertIn(self.s2.data, res.data)
        self.assertIn(self.s3.data, res.data)
        self.assertNotIn(self.s4.data, res.data)
        self.assertEqual(len(res.data), 3)

        params = {'modified_to': self.yesterday}
        res = self.client.get(url, params)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(self.s1.data, res.data)
        self.assertNotIn(self.s2.data, res.data)
        self.assertNotIn(self.s3.data, res.data)
        self.assertNotIn(self.s4.data, res.data)
        self.assertEqual(len(res.data), 0)

        params = {'created_to': self.tomorrow, 'title': 'Wednesday'}
        res = self.client.get(url, params)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(self.s1.data, res.data)
        self.assertNotIn(self.s2.data, res.data)
        self.assertIn(self.s3.data, res.data)
        self.assertNotIn(self.s4.data, res.data)
        self.assertEqual(len(res.data), 1)

        params = {'modified_to': self.tomorrow, 'title': 'other menu'}
        res = self.client.get(url, params)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(self.s1.data, res.data)
        self.assertNotIn(self.s2.data, res.data)
        self.assertNotIn(self.s3.data, res.data)
        self.assertNotIn(self.s4.data, res.data)
        self.assertEqual(len(res.data), 0)

    def test_get_sorted_menus_by_name_or_by_dish_count(self):
        """Test sorting menu by name or by number of dishes in menu."""
        url = MENU_URL

        res = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 3)
        self.assertEqual(res.data[0]['id'], self.menu1.id)
        self.assertEqual(res.data[1]['id'], self.menu2.id)
        self.assertEqual(res.data[2]['id'], self.menu3.id)

        res = self.client.get(url, {'ordering': '-dish_count'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 3)
        self.assertEqual(res.data[0]['id'], self.menu3.id)
        self.assertEqual(res.data[1]['id'], self.menu1.id)
        self.assertEqual(res.data[2]['id'], self.menu2.id)
