from django.core.management.base import BaseCommand
from config.cron import update_product_status


class Command(BaseCommand):
    """
    Update product status LOAN to AFTER_MATURITY and set sell_price
    """

    def handle(self, *args, **options):
        """
        Update product status LOAN to AFTER_MATURITY and set sell_price
        :param args: None
        :param options: None
        :return: None
        """
        update_product_status()


# class Command(BaseCommand):
#     def get_week_delta(self, start_date):
#         result = (date.today() - start_date.date()).days // 7 + 1
#         return result
#
#     def handle(self, *args, **options):
#         qs_after_maturity = Product.objects.filter(models.Q(status=ProductStatusOrData.LOAN.name))
#
#         for loan in qs_after_maturity:
#             loan.status = (
#                 ProductStatusOrData.LOAN.name
#                 if self.get_week_delta(loan.date_extend) <= loan.rate_times
#                 else ProductStatusOrData.AFTER_MATURITY.name
#             )
#             loan.sell_price = utils.get_sell_price(
#                 rate=loan.interest_rate_or_quantity, buy_price=loan.buy_price,
#                 times=self.get_week_delta(loan.date_extend)
#             )
#             loan.save()
#
#         self.stdout.write(self.style.SUCCESS("Successfully Updated Loans"))
