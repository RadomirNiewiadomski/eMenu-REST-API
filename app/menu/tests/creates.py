from decimal import Decimal

from core.models import (
    Menu,
    Dish,
)


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
