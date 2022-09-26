from django.contrib import admin

from .models import Customer, CustomUser, MortgageContract, Product, Shop

admin.site.register(Shop)
admin.site.register(Customer)
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(MortgageContract)
