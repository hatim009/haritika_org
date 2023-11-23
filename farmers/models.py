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

    farmer_id = models.BigAutoField(primary_key=True)
    id_hash = models.CharField(max_length=128, unique=True, validators=[MinLengthValidator(128)])
    name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = PhoneNumberField(null=False, blank=False)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    address = models.CharField(max_length=150)
    state_code = models.ForeignKey('local_directories.StatesDirectory', on_delete=models.DO_NOTHING)
    district_code = models.ForeignKey('local_directories.DistrictsDirectory', on_delete=models.DO_NOTHING)
    block_code = models.ForeignKey('local_directories.BlocksDirectory', on_delete=models.DO_NOTHING)
    village_code = models.ForeignKey('local_directories.VillagesDirectory', on_delete=models.DO_NOTHING)
    id_front_image_s3_location = models.TextField()
    id_back_image_s3_location = models.TextField()
    income_level = models.CharField(max_length=20, choices=IncomeLevel.choices)
    added_by = models.CharField(max_length=150, editable=False)
    added_on = models.DateTimeField(auto_now_add=True)
    last_edited_by = models.CharField(max_length=150)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("farmer")
        verbose_name_plural = _("farmers")
        db_table = "farmers"


