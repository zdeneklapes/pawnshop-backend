import uuid

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=255)


class Customer(models.Model):
    GENDERS = (("M", "Male"), ("F", "Female"))

    personal_identification_number = models.CharField(max_length=255, primary_key=True)
    full_name = models.CharField(max_length=255)
    identity_card_number = models.CharField(max_length=255)
    residence = models.CharField(max_length=255)
    citizenship = models.CharField(max_length=255)
    place_of_birth = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDERS)


# class BaseDates(models.Model):
#     creation_date = models.DateTimeField(primary_key=True)  # when product was taken into custody
#     extended_deadline_date = models.DateTimeField(null=True)  # when mortgage contract was extend


class Product(models.Model):
    description = models.TextField()
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()

    creation_date = models.DateTimeField(
        primary_key=True
    )  # when product was taken into custody
    extended_deadline_date = models.DateTimeField(
        null=True
    )  # when mortgage contract was extend
    end_date = models.DateTimeField(null=True)  # last day of contract


class MortgageContract(models.Model):
    # TODO: father wants ID as incrementing number,
    #  but there could be a problem, so ID+FROM_DATE must create Primary Key:
    #  e.g.: 1 customer have contract from 2022 and another customer will come
    #  in 2023 and because all contracts start from 00001 as year begins so the ids can become same
    id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField()  # when product was taken into custody

    extended_deadline_date = models.DateTimeField(
        null=True
    )  # when mortgage contract was extend
    end_date = models.DateTimeField()  # last day of contract

    buy_price = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=3, decimal_places=1)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    person = models.ForeignKey(to=Customer, on_delete=models.CASCADE)

    # Source: https://stackoverflow.com/a/16800384/14471542
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id", "creation_date"],
                name="unique_id_creation_date_combination",
            )
        ]


class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    open_hours = models.TimeField()
    close_hours = models.TimeField()
