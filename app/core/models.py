"""
Database models.
"""
import uuid
import os

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


def dish_image_file_path(instance, filename):
    """Generate file path for new dish image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'dish', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Dish(models.Model):
    title = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    price = models.DecimalField(_('Price'), max_digits=5, decimal_places=2)
    time_minutes = models.IntegerField(_('Preparation time in min'))
    vegetarian = models.BooleanField(_('Is vegetarian'))
    created_date = models.DateField(_('Created'), auto_now_add=True)
    modified_date = models.DateField(_('Modified'), auto_now=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to=dish_image_file_path)

    class Meta:
        verbose_name = _("Dish")
        verbose_name_plural = _("Dishes")

    def __str__(self):
        return self.title


class Menu(models.Model):
    """Menu object."""
    title = models.CharField(_('Menu name'), unique=True, max_length=255)
    description = models.TextField(_('Description'), blank=True)
    dishes = models.ManyToManyField(Dish, verbose_name=_('Dish'))
    created_date = models.DateField(_('Created'), auto_now_add=True)
    modified_date = models.DateField(_('Modified'), auto_now=True, blank=True)

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

    def __str__(self):
        return self.title
