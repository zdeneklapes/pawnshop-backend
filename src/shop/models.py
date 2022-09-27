from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    open_hours = models.TimeField()
    close_hours = models.TimeField()

    class Meta:
        app_label = "shop_app"

    def __str__(self):
        return self.name.name
