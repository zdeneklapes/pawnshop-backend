from django.contrib import admin
from django.contrib.auth.models import Permission

from . import models


# ######################################################################################################################
# Authentication
# ######################################################################################################################
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AttendantProfile)
class AttendantProfileAdmin(admin.ModelAdmin):
    pass


# ######################################################################################################################
# Permissions
# ######################################################################################################################


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
