"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from authentication.models.choices import UserGroupChoice
from django.contrib import auth
from django.contrib.auth import get_user_model


def all_available_permissions():
    """
    Source: https://timonweb.com/django/how-to-get-a-list-of-all-user-permissions-available-in-django-based-project/
    """
    permissions = set()

    # We create (but not persist) a temporary superuser and use it to
    # game the system and pull all permissions easily.
    tmp_superuser = get_user_model()(is_active=True, is_superuser=True)

    # We go over each AUTHENTICATION_BACKEND and try to
    # fetch a list of permissions
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(tmp_superuser))

    # Make a unique list of permissions sorted by permission name.
    sorted_list_of_permissions = sorted(list(permissions))
    return sorted_list_of_permissions


group_permission = {
    UserGroupChoice.ADMIN_ADMIN: [*all_available_permissions()],
    UserGroupChoice.ADMIN: [
        #
        "authentication.add_attendantprofile",
        "authentication.change_attendantprofile",
        "authentication.change_user",
        "authentication.delete_attendantprofile",
        "authentication.view_attendantprofile",
        "authentication.view_user",
        #
        "customer.add_customerprofile",
        "customer.change_customerprofile",
        "customer.delete_customerprofile",
        "customer.view_customerprofile",
        #
        "product.add_product",
        "product.change_product",
        "product.view_product",
        #
        "statistic.add_statistic",
        "statistic.reset_profit",
        "statistic.view_cash_amount",
        "statistic.view_daily_stats",
        "statistic.view_statistic",
    ],
    UserGroupChoice.ATTENDANT: [
        #
        "authentication.change_attendantprofile",
        #
        "customer.add_customerprofile",
        "customer.change_customerprofile",
        "customer.delete_customerprofile",
        "customer.view_customerprofile",
        #
        "product.add_product",
        "product.change_product",
        "product.view_product",
        #
        "statistic.view_statistic",
        "statistic.view_cash_amount",
    ],
}


class Command(BaseCommand):
    """
    Command to create groups and add permissions to them
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--print", "-p", action="store_true", dest="print", default=False, help="Prints the permissions and groups"
        )

    def handle(self, *args, **options):
        """
        Create groups and add permissions to them
        :param args:
        :param options: print
        :return: None
        """
        for group in UserGroupChoice.names:
            new_group, _ = Group.objects.get_or_create(name=group)
            for permission in group_permission[group]:
                if options["print"]:
                    print(f"For Group {group} adding permission: {permission}")
                try:
                    app_label, codename = permission.split(".")
                    _perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                    new_group.permissions.add(_perm)
                except Permission.DoesNotExist:
                    logging.warning(f"Permission not found with name '{permission}'.")
                    continue
