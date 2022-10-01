import requests
from rest_framework import mixins, permissions, response, viewsets

from product import models, serializers
from product.models import Product


def create_data(request: requests.Request):
    return {
        # "user": request.user.id,
        "customer": {
            "id_person_number": request.data['birth_id'],
            "full_name": request.data['name'],
            "id_card_number": request.data["personal_id"],
            "id_card_number_expiration_date": request.data["personal_id_date"],
            "residence": request.data["address"],
            "nationality": request.data["nationality"],
            "place_of_birth": request.data["birth_place"],
            "sex": request.data['sex']
        },
        "status": request.data['status'],
        "rate": request.data['interest_rate_or_amount'],
        "description": request.data['product_name'],
        "buy_price": request.data['product_buy'],
        "sell_price": request.data['product_sell'],
        "quantity": request.data["quantity"] if 'quantity' in request.data else 1,
    }


class CreateProduct(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request: requests.Request, *args, **kwargs):
        request.data.update(create_data(request))
        super().create(request)


class LoanViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.LoanSerializer


class OfferViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.OfferSerializer


class AfterMaturityViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.AfterMaturitySerialzier
