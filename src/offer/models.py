from django.db import models

from authentication.models import CustomerProfile
from product.models import Product
from shop.models import Shop


class Offer(models.Model):
    #
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE)
    person = models.OneToOneField(to=CustomerProfile, on_delete=models.CASCADE)
    shop = models.OneToOneField(to=Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
