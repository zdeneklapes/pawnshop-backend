from django.db import models


class UserRoleChoice(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    ATTENDANT = "ATTENDANT", "Attendant"
