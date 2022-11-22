from django.contrib import admin

from .models.models import Product


@admin.register(Product)
class ProductConfigAdmin(admin.ModelAdmin):
    pass
