from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# User = get_user_model()


class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, unique=True)
    town = models.CharField(max_length=255)
    phone_number = PhoneNumberField(max_length=20, unique=True)

    open_hours = models.TimeField()
    close_hours = models.TimeField()

    is_active = models.BooleanField(default=True)  # Can shop provide services?
