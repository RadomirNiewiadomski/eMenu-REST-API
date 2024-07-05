"""
Command to create initial data.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from menu.tests.creates import create_dish, create_menu
from menu.models import Menu


class Command(BaseCommand):
    """Command to create initial data to db."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        if not Menu.objects.filter(title='Quick breakfast'):
            menu1 = create_menu(title='Quick breakfast',
                                description='Really quick breakfast.')
            dish1 = create_dish(title='Sandwich',
                                description='Sandwich with ham',
                                price=Decimal('4.00'),
                                time_minutes=2,
                                vegetarian=False)
            dish2 = create_dish(title='Coffee',
                                price=Decimal('3.00'),
                                time_minutes=1,
                                vegetarian=True)
            menu1.dishes.add(dish1, dish2)
            menu1.save()

        if not Menu.objects.filter(title='Sweet menu'):
            menu2 = create_menu(title='Sweet menu')
            dish3 = create_dish(title='Pancaked',
                                price=Decimal('8.00'),
                                time_minutes=20,
                                vegetarian=True)
            menu2.dishes.add(dish3)
            menu2.save()

        if not Menu.objects.filter(title='French cuisine'):
            menu3 = create_menu(title='French cuisine',
                                description='French dishes.')
            dish4 = create_dish(title='Baguette with garlic',
                                price=Decimal('4.50'),
                                time_minutes=5,
                                vegetarian=True)
            dish5 = create_dish(title='Fresh coffee',
                                price=Decimal('3.00'),
                                time_minutes=2,
                                vegetarian=True)
            menu3.dishes.add(dish4, dish5)
            menu3.save()

        if not Menu.objects.filter(title='Exclusive menu card'):
            menu4 = create_menu(title='Exclusive menu card',
                                description='Luxury dishes.')
            dish6 = create_dish(title='Ham',
                                price=Decimal('14.00'),
                                time_minutes=35,
                                vegetarian=False)
            dish7 = create_dish(title='Onion soup',
                                price=Decimal('13.00'),
                                time_minutes=40,
                                vegetarian=True)
            menu4.dishes.add(dish6, dish7)
            menu4.save()
