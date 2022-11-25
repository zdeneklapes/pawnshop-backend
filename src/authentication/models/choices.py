from django.db import models


class UserGroupChoice(models.TextChoices):
    """
    Choices for User Group and their permissions
    """

    ADMIN_ADMIN = "ADMIN_ADMIN", "Root Admin"
    ADMIN = "ADMIN", "Admin"
    ATTENDANT = "ATTENDANT", "Attendant"
