"""
Database models.
"""
from django.conf import settings
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new ussr."""
        if not email:
            raise ValueError("email is required.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser."""
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


class Contract(models.Model):
    """Contrat object."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          unique=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    level = models.IntegerField(default=1, blank=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(3),
    ])
    gardens = models.ManyToManyField('Garden')

    def __str__(self):
        return self.name


class Garden(models.Model):
    """Garden for contract."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    level = models.IntegerField(default=1, blank=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(3),
        ])
    plants = models.ManyToManyField('Plant')

    def __str__(self):
        return self.name


class Plant(models.Model):
    garden_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    soil_moisture_percentage = models.FloatField(default=0)
    fertilizer_per_meter = models.FloatField(default=0)
    height = models.FloatField(default=0)
    number_or_stems = models.FloatField(default=0)
    health = models.FloatField(default=0)
    has_plant = models.BooleanField(default=True)
    soil_cohesity = models.FloatField(default=0)
    disease = models.FloatField(default=0)
    insects_per_meter = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name
