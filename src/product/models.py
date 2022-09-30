from datetime import date

from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Product(models.Model):
    #
    description = models.TextField()
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    # Dates
    date_create = models.DateTimeField(auto_now_add=True)
    date_extended_deadline = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)  # return/sell

    def update_sell_price_based_on_week(self, rate) -> models.Model:
        if self.date_extended_deadline:
            d1 = date(self.date_extended_deadline.year,
                      self.date_extended_deadline.month,
                      self.date_extended_deadline.day)
        else:
            d1 = date(self.date_create.year,
                      self.date_create.month,
                      self.date_create.day)
        d2 = date.today()
        weeks = (d2 - d1).days // 7 + 1
        sell_price = (float(rate) / 100) * weeks * self.buy_price + self.buy_price

        # Rounded to 5, e.g.: 1004 => 1005, 1006 => 1010
        sell_price_rounded = (
            sell_price if (sell_price % 5) == 0 else sell_price - ((sell_price % 5) - 5)
        )

        self.sell_price = sell_price_rounded
        self.save()
