from django.contrib import admin
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerAdmin(admin.ModelAdmin):
    pass
