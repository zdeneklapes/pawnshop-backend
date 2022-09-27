from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """Source: https://github.com/jod35/Pizza-delivery-API-Django"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please enter an email address")

        email = self.normalize_email(email)

        new_user = self.model(email=email, **extra_fields)

        new_user.set_password(password)

        new_user.save()

        return new_user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = PhoneNumberField(max_length=15, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", "phone_number"]


class Rights(models.Model):
    user = models.ForeignKey(User)
    action_edit_custom_user = models.BooleanField()
    action_detailed_stats = models.BooleanField()
    action_day_stats = models.BooleanField()
    action_edit_subject = models.BooleanField()
    action_edit_all_item = models.BooleanField()
    action_edit_date = models.BooleanField()
    action_edit_sell_price = models.BooleanField()
    action_edit_cash_register = models.BooleanField()
    action_can_divide = models.BooleanField()
    action_move_to_pawnshop_tab = models.BooleanField()
    action_complete_win = models.BooleanField()
    action_getout_without_eet = models.BooleanField()
    action_price_in_stats = models.BooleanField()
    # action_have_access_to_shop = models.ManyToManyField(Shop) # TODO: Create Shop model


# class Shop(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     district = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255)
#     open_hours = models.TimeField()
#     close_hours = models.TimeField()
#
#
# class Statistics(models.Model):
#     date = models.DateTimeField(auto_now_add=True)
#     description = models.CharField(max_length=255)
#     # TODO: FK of the object which has changed
#
#
# class Customer(models.Model):
#     GENDERS = (("M", "Male"), ("F", "Female"))
#
#     personal_identification_number = models.CharField(max_length=255, primary_key=True)
#     full_name = models.CharField(max_length=255)
#     identity_card_number = models.CharField(max_length=255)
#     residence = models.CharField(max_length=255)
#     citizenship = models.CharField(max_length=255)
#     place_of_birth = models.CharField(max_length=255)
#     gender = models.CharField(max_length=1, choices=GENDERS)
#
#
# class Product(models.Model):
#     description = models.TextField()
#     buy_price = models.PositiveIntegerField()
#     sell_price = models.PositiveIntegerField()
#     quantity = models.PositiveIntegerField(default=1)
#     shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
#
#     creation_date = models.DateTimeField(
#         primary_key=True
#     )  # when product was taken into custody
#     extended_deadline_date = models.DateTimeField(
#         null=True
#     )  # when mortgage contract was extend
#     end_date = models.DateTimeField(null=True)  # last day of contract
#
#
# class MortgageContract(models.Model):
#     # TODO: father wants ID as incrementing number,
#     #  but there could be a problem, so ID+FROM_DATE must create Primary Key:
#     #  e.g.: 1 customer have contract from 2022 and another customer will come
#     #  in 2023 and because all contracts start from 00001 as year begins so the ids can become same
#     # Source: https://stackoverflow.com/a/71909815/14471542
#
#     @classmethod
#     def next_number(self):
#         return self._base_manager.filter(date__year=now().year).count() + 1
#
#     num_contract_in_year = models.PositiveIntegerField(
#         default=next_number, editable=False
#     )
#     creation_date = models.DateTimeField()  # when product was taken into custody
#
#     extended_deadline_date = models.DateTimeField(
#         null=True
#     )  # when mortgage contract was extend
#     end_date = models.DateTimeField()  # last day of contract
#
#     buy_price = models.PositiveIntegerField()
#     rate = models.DecimalField(max_digits=3, decimal_places=1)
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
#     person = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
#
#     # Source: https://stackoverflow.com/a/16800384/14471542
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["id", "creation_date"],
#                 name="unique_id_creation_date_combination",
#             )
#         ]
