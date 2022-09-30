from django.db import models

from authentication.models import CustomerProfile, User
from product.models import Product
from shop.models import Shop


class Offer(models.Model):
    #
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
