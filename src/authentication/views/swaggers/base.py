# pylint: disable=E1101
from drf_yasg import openapi

import django_filters


class AuthBaseSwagger(django_filters.FilterSet):
    create = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        in_=openapi.IN_BODY,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "verify_password": openapi.Schema(type=openapi.TYPE_STRING),
            "old_password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
    update = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        in_=openapi.IN_BODY,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "verify_password": openapi.Schema(type=openapi.TYPE_STRING),
            "old_password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )


class UserQPSwagger(AuthBaseSwagger):
    pass


class AttendantQPSwagger(AuthBaseSwagger):
    pass
