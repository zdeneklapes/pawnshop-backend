from django.utils import timezone

import requests
from rest_framework import mixins, viewsets

from product.serializers.product import ProductSerializer
from product.models import models, choices
from statistic.serializers import StatisticSerializer
from statistic.models.choices import StatisticOperation


class CreateProductViewSet(
    mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    def create(self, request: requests.Request, *args, **kwargs):
        response = super().create(request)  # to internal_repre -> to to_repre
        try:
            StatisticSerializer.save_statistics(
                price=response.data["buy_price"],
                operation=StatisticOperation.LOAN_CREATE.name,
                user=response.data["user"],
                product=response.data["id"],
            )
        except AssertionError as e:
            print(f"Error {CreateProductViewSet.create.__qualname__}: {e}")
        return response

    # def retrieve(self, request, *args, **kwargs):
    #     response = super(CreateProductViewSet, self).retrieve(request)
    #     return response


class LoanViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.get_loans()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    def list(self, request, *args, **kwargs):
        return super().list(request)


class OfferViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Product.objects.get_offers()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    def list(self, request, *args, **kwargs):
        return super().list(request)


class AfterMaturityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Product.objects.get_after_maturity()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment


class ExtendLoanViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["patch"]
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment


    # def create_data(self, loan: models.Product):
    #     return {
    #         "status": models.ProductStatus.LOAN.name,
    #         "sell_price": utils.get_sell_price(rate=loan.rate, buy_price=loan.buy_price),
    #         "date_extend": timezone.now(),
    #     }

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request)


class ReturnLoanViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["patch"]

    # permission_classes = [permissions.IsAuthenticated]

    def create_data(self, request: requests.Request):
        return {"status": choices.ProductStatus.INACTIVE_LOAN.name, "date_end": timezone.now()}

    def partial_update(self, request, *args, **kwargs):
        # TODO: Return only LOAN and AFTER_MATURITY
        request.data.update(self.create_data(request))
        return super().partial_update(request)


class LoanToBazarViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ["patch"]

    # permission_classes = [permissions.IsAuthenticated]

    def create_data(self, request: requests.Request):
        return {"status": choices.ProductStatus.OFFER.name, "sell_price": request.data["product_sell"]}

    def partial_update(self, request, *args, **kwargs):
        # TODO: Move only AFTER_MATURITY
        request.data.update(self.create_data(request))
        return super().partial_update(request)
