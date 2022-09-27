from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = [""]
    # fieldsets = None


admin.site.register(User, UserAdmin)
