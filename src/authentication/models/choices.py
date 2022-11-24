from django.db import models


class UserRoleChoice(models.TextChoices):
    ADMIN_ADMIN = "ADMIN_ADMIN", "Root Admin"
    ADMIN = "ADMIN", "Admin"
    ATTENDANT = "ATTENDANT", "Attendant"
