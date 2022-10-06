# pylint: disable=E1101
from typing import Optional

from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.views import View
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
import django_filters

from product.serializers import product as product_serializers
from product.models import models
from product.models.choices import ProductStatus, ProductQPData
from statistic.serializers.statistic import StatisticDefaultSerializer
from statistic.models.choices import StatisticDescription
from common.exceptions import BadQueryParam
from statistic.models.choices import StatisticQPData


class ProductQPSwagger(django_filters.FilterSet):
    data = openapi.Parameter(
        name="data",
        in_=openapi.IN_QUERY,
        description=f"Operation Type: " f"{ProductQPData.SHOP_STATS.name}",
        type=openapi.TYPE_STRING,
    )
    operation = openapi.Parameter(
        name="operation",
        in_=openapi.IN_QUERY,
        description=f"Operation Type: "
        f"{StatisticDescription.LOAN_EXTEND.name}, "
        f"{StatisticDescription.LOAN_RETURN.name}, "
        f"{StatisticDescription.LOAN_TO_OFFER.name}",
        type=openapi.TYPE_STRING,
    )
    status = openapi.Parameter(
        name="status",
        in_=openapi.IN_QUERY,
        description=f"Product status: "
        f"{ProductStatus.LOAN.name}, "
        f"{ProductStatus.OFFER.name}, "
        f"{ProductStatus.AFTER_MATURITY.name}",
        type=openapi.TYPE_STRING,
    )


@method_decorator(
    name="list", decorator=swagger_auto_schema(manual_parameters=[ProductQPSwagger.status, ProductQPSwagger.data])
)
@method_decorator(name="create", decorator=swagger_auto_schema(manual_parameters=[]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(manual_parameters=[]))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(manual_parameters=[ProductQPSwagger.operation]))
class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = product_serializers.ProductSerializer
    http_method_names = ["get", "post", "patch"]

    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    def parse_status_request(self):
        if "status" not in self.request.query_params:
            return None

        if self.request.query_params["status"] in ProductStatus.values:  # pylint: disable=E1101:
            return self.request.query_params["status"]

        return None

    def parse_data_request(self) -> Optional[str]:
        if "data" not in self.request.query_params:
            return None

        if self.request.query_params["data"] == ProductQPData.SHOP_STATS.name:  # pylint: disable=E1101:
            return self.request.query_params["data"]

        return None

    def parse_operation_request(self) -> Optional[str]:
        if "operation" not in self.request.query_params:
            return None

        if self.request.query_params["operation"] not in StatisticQPData.values:  # pylint: disable=E1101:
            return None

        return self.request.query_params["operation"]

    def get_queryset(self):
        status_choice = self.parse_status_request()
        data_choice = self.parse_data_request()

        if status_choice:
            return models.Product.objects.get_product_by_status(status_choice)

        if data_choice == ProductQPData.SHOP_STATS.name:
            return models.Product.objects.get_shop_state()

        return super().get_queryset()

    def get_serializer_class(self):
        operation = self.parse_operation_request()
        data_choice = self.parse_data_request()

        if data_choice == ProductQPData.SHOP_STATS.name:
            return product_serializers.ShopStateSerializer

        if operation == StatisticDescription.LOAN_EXTEND.name:
            return product_serializers.LoanExtendSerializer

        if operation == StatisticDescription.LOAN_RETURN.name:
            return product_serializers.LoanReturnSerializer

        if operation == StatisticDescription.LOAN_TO_OFFER.name:
            return product_serializers.LoanToOfferSerializer

        return super().get_serializer_class()

    # Request Handlers
    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request)

    def create(self, request: Request, *args, **kwargs):
        response: Response = super().create(request)  # to internal_repre -> to to_repre
        try:
            StatisticDefaultSerializer.save_statistics(
                price=-response.data["buy_price"],
                operation=StatisticDescription.LOAN_CREATE.name,
                user=request.data["user"],  # TODO: change to user: response.user.id
                product=response.data["id"],
            )
        except AssertionError as e:
            return Response(
                data={"error": f"{ProductViewSet.create.__qualname__} - {e} - statistics"}, status=response.status_code
            )
        return response

    def patial_update_save_statistics(self, request: Request, buy_price_prev: int, sell_price_prev: int):
        # Validate
        operation, price = StatisticDescription.validate_operation(request, buy_price_prev, sell_price_prev)

        # Save Statistics
        StatisticDefaultSerializer.save_statistics(
            price=price,
            operation=operation,
            user=request.user.id,
            product=request.parser_context["kwargs"]["pk"],
        )

    def partial_update(self, request: Request, *args, **kwargs):
        # Store previous price
        loan = models.Product.objects.get(pk=request.parser_context["kwargs"]["pk"])
        sell_price_prev = loan.sell_price
        buy_price_prev = loan.buy_price

        try:
            response = super().partial_update(request)
            self.patial_update_save_statistics(request, buy_price_prev, sell_price_prev)
        except BadQueryParam as e:
            return Response(
                data={"details": f"Bad query params - {e}"}, status=BadQueryParam.status_code, exception=True
            )
        return response


data = {
    "customer": {
        "full_name": "a b",
        "residence": "Cejl 222",
        "sex": "M",
        "nationality": "SK",
        "personal_id": "0000000000",
        "personal_id_expiration_date": "2023-02-02",
        "birthplace": "Prha",
        "id_birth": "000000/0001",
    },
    "user": 1,
    "status": "LOAN",
    "interest_rate_or_quantity": 10,
    "inventory_id": 3,
    "product_name": "watch",
    "buy_price": 3000,
    "sell_price": 4200,
}


class ContractPdf(View):
    def render_to_pdf(self, template_src, context_dict=None, encoding="UTF-8"):
        if context_dict is None:
            context_dict = {}
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(html, result, encoding=encoding)
        # pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type="application/pdf")
            filename = "loan_contract.pdf"
            content = f"inline; filename={filename}"
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Not found")

    def render_to_pdf_2(self, template_src, context_dict=None):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        html_encoded = str(html).encode("UTF-8")
        pdf = pisa.pisaDocument(html_encoded, result, encoding="UTF-8")
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type="application/pdf")
        return HttpResponse("We had some errors")

    def get(self, request, *args, **kwargs):
        template2 = "documents/test1.html"
        return self.render_to_pdf_2(template2)
