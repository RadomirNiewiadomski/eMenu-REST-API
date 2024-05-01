"""
Django admin customization.
"""
from django.contrib import admin

from menu.models import (
    Menu,
    Dish,
)


class MenuAdmin(admin.ModelAdmin):
    list_filter = ['title', 'created_date', 'modified_date']
    list_display = ['title']


admin.site.register(Menu, MenuAdmin)
admin.site.register(Dish)
