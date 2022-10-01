from django.core.management.base import BaseCommand
from product.models.models import Product
from product.models.choices import ProductStatus
from datetime import date
from common import utils


class Command(BaseCommand):
    def get_week_delta(self, start_date):
        result = (date.today() - start_date.date()).days // 7 + 1
        return result

    def handle(self, *args, **options):
        qs_after_maturity = Product.objects.filter(status=ProductStatus.LOAN.name) | Product.objects.filter(
            status=ProductStatus.AFTER_MATURITY.name
        )

        for loan in qs_after_maturity:
            loan.status = (
                ProductStatus.LOAN.name
                if self.get_week_delta(loan.date_extend) <= loan.rate_times
                else ProductStatus.AFTER_MATURITY.name
            )
            loan.sell_price = utils.get_sell_price(
                rate=loan.rate, buy_price=loan.buy_price, times=self.get_week_delta(loan.date_extend)
            )
            loan.save()

        self.stdout.write(self.style.SUCCESS("Successfully Updated Loans"))
