from django.db import models

# User = get_user_model()


class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, unique=True)
    town = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, unique=True)

    open_hours = models.TimeField()
    close_hours = models.TimeField()

    is_active = models.BooleanField(default=True)  # Can shop provide services?
