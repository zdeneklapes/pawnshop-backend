from rest_framework.exceptions import APIException
from rest_framework import status


class BadQueryParam(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad query_prams for updating product status"
    default_code = "bas_request"
