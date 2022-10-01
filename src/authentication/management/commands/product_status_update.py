from django.core.management.base import BaseCommand
from product.models import Product
from product.choices import ProductStatus
from datetime import date, timedelta
from common import utils


class Command(BaseCommand):
    def handle(self, *args, **options):
        def start_date():
            startdate = date.today() - timedelta(weeks=4)
            return startdate

        qs_after_maturity = Product.objects.filter(date_create__gte=start_date()) & Product.objects.filter(
            date_extend__gte=start_date()
        )

        for loan in qs_after_maturity:
            loan.update(
                status=ProductStatus.AFTER_MATURITY.name,
                sell_price=utils.get_sell_price(rate=loan.rate, buy_price=loan.buy_price),
            )

        self.stdout.write(self.style.SUCCESS("Successfully Updated Loans"))
