# Register your models here.
from django.contrib import admin

from . import models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    pass
    # list_display = ("name", "owner", "location", "phone_number")
