from django.db import models


class CustomerProfile(models.Model):
    GENDERS_CHOICES = (("M", "Male"), ("F", "Female"))

    id_birth = models.CharField(primary_key=True, max_length=255)
    full_name = models.CharField(max_length=255)
    personal_id = models.CharField(max_length=255)
    personal_id_expiration_date = models.DateField()
    residence = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    birthplace = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=GENDERS_CHOICES)
