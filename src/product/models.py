from datetime import datetime, timedelta, date

from django.db import models

from authentication.models import CustomerProfile, User
from shop.models import Shop


# def next_number():
#     """Source: https://stackoverflow.com/a/71909815/14471542"""
# return Loan.objects.filter(date_created__year=datetime.now().year).count() + 1


class LoanManager(models.Manager):
    @property
    def start_date(self):
        startdate = date.today() - timedelta(weeks=4)
        return startdate

    def get_offers(self):
        pass

    def get_loans(self):
        qs_products = Product.objects.filter(
            date_create__gte=self.start_date
        ) | Product.objects.filter(date_extended_deadline__gte=self.start_date)
        return (
            super(LoanManager, self)
            .get_queryset()
            .filter(product__in=qs_products.values("id"), is_active=True)
        )

    def after_maturity(self):
        qs_products = Product.objects.filter(
            date_create__lt=self.start_date
        ) | Product.objects.filter(date_extended_deadline__lt=self.start_date)
        return (
            super(LoanManager, self)
            .get_queryset()
            .filter(product__in=qs_products.values("id"), is_active=True)
        )


class RateFrequency(models.TextChoices):
    DAY = "DAY", "Day"
    WEEK = "WEEK", "Week"
    YEAR = "YEAR", "Year"


class Status(models.TextChoices):
    BUY = "OFFER", "Offer"
    LOAN = "LOAN", "Loan"
    AFTER_MATURITY = "AFTER_MATURITY" "After_maturity"
    INACTIVE = "INACTIVE", "Inactive"


class Product(models.Model):
    status = models.CharField(max_length=50, choices=Status.choices)

    # Managers
    objects = LoanManager()

    # FK
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)

    # Rate
    rate_frequency = models.CharField(max_length=50, choices=RateFrequency.choices, default="WEEK")
    rate_times = models.PositiveIntegerField(default=4)
    rate = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    # Product
    description = models.TextField()
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField(null=True)  # Cron
    quantity = models.PositiveIntegerField(default=1)

    # Dates
    date_create = models.DateTimeField(auto_now_add=True)
    date_extend = models.DateTimeField(null=True)
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
        sell_price_rounded = (sell_price if (sell_price % 5) == 0 else sell_price - ((sell_price % 5) - 5))

        self.sell_price = sell_price_rounded
        self.save()

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.rate_fequency = RateFrequency.WEEK
    #         self.rate_times = 4
    #         return super().save(*args, **kwargs)
