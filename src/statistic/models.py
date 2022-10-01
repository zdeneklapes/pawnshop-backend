from django.db import models

from authentication.models import User
from product.models import Product


class StatisticOperation(models.TextChoices):
    VYBER = "VYBER", "Vyber"
    ZASTAVA = "ZASTAVA", "Zastava"
    PRODLOUZENI = "PRODLOUZENI", "Prodlouzeni"


class Statistic(models.Model):
    # FK
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    #
    description = models.CharField(max_length=255, choices=StatisticOperation.choices)
