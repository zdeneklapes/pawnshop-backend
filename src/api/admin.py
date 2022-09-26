from django.contrib import admin

from .models import Customer, CustomUser, MortgageContract, Product, Shop


class ShopAdmin(admin.ModelAdmin):
    fields = ["name", "address", "district", "phone", "open_hours", "close_hours"]
    # fieldsets = None


class CustomerAdmin(admin.ModelAdmin):
    pass


class CustomUserAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class MortageContractAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)
# TODO: admin.site.register(Customer)
# TODO: admin.site.register(CustomUser)
# TODO: admin.site.register(Product)
# TODO: admin.site.register(MortgageContract)
