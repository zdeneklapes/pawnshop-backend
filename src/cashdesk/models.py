from django.db import models

from authentication.models import User
from shop.models import Shop


class CashDesk(models.Model):
    #
    person = models.OneToOneField(to=User, on_delete=models.CASCADE)
    shop = models.OneToOneField(to=Shop, on_delete=models.CASCADE)

    #
    actual_amount = models.IntegerField()
    change = models.IntegerField()

    #
    creation_date = models.DateTimeField()
