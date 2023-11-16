from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Farmer(models.Model):
    class Category(models.TextChoices):
        GENERAL = 'GENERAL', _('General')
        SC = 'SC', _('ScheduleCastes')
        ST = 'ST', _('ScheduleTribes')
        OBC = 'OBC', _('OtherBackwardClass')

    class Gender(models.TextChoices):
        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')
        OTHERS = 'OTHERS', _('Others')

    class IncomeLevel(models.TextChoices):
        LESS_THAN_30K = '<30k', _('<30k')
        BETWEEN_30K_AND_50K = '30k-50k', _('30k-50k')
        BETWEEN_50K_AND_80K = '50k-80k', _('50k-80k')
        GREATER_THAN_80K = '>80k', _('>80k')

    farmer_id = models.CharField(max_length=128, primary_key=True, validators=[MinLengthValidator(128)])
    name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    address = models.CharField(max_length=150)
    block = models.CharField(max_length=10)
    pincode = models.CharField(max_length=8)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    id_front_image_link = models.TextField()
    id_back_image_link = models.TextField()
    income_level = models.CharField(max_length=20, choices=IncomeLevel.choices)

    class Meta:
        verbose_name = _("farmer")
        verbose_name_plural = _("farmers")
        db_table = "farmers"


