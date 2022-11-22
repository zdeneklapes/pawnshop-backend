from django.db import models


class CustomGroup(models.TextChoices):
    ADMIN_ADMIN = "ADMIN_ADMIN", "Root Admin"
    ADMIN = "ADMIN", "Admin"
    ATTENDANT = "ATTENDANT", "Attendant"
