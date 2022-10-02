from django.contrib import admin

from . import models

# Note all Usertypes must be registered, otherwise error
admin.site.register(models.User)
admin.site.register(models.AttendantProfile)
