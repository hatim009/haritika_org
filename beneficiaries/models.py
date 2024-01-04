from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Beneficiary(models.Model):

    class Gender(models.TextChoices):
        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')
        OTHERS = 'OTHERS', _('Others')

    beneficiary_id = models.BigAutoField(primary_key=True)
    id_hash = models.CharField(max_length=128, unique=True, validators=[MinLengthValidator(128)])
    profile_photo = models.ForeignKey('files_manager.File', db_column='profile_photo', related_name='beneficiary_profile_photo', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    guardian = models.ForeignKey('farmers.Farmer', related_name='beneficiaries', on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = PhoneNumberField(null=False, blank=False)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    address = models.CharField(max_length=150)
    village = models.ForeignKey('local_directories.VillagesDirectory', on_delete=models.DO_NOTHING)
    id_front_image = models.ForeignKey('files_manager.File', db_column='id_front_image', related_name='beneficiary_id_front_image', on_delete=models.DO_NOTHING)
    id_back_image = models.ForeignKey('files_manager.File', db_column='id_back_image', related_name='beneficiary_id_back_image', on_delete=models.DO_NOTHING)
    added_by = models.ForeignKey('users.User', editable=False, related_name='beneficiary_added_by', on_delete=models.DO_NOTHING)
    added_on = models.DateTimeField(auto_now_add=True)
    last_edited_by = models.ForeignKey('users.User', related_name='beneficiary_last_edited_by', on_delete=models.DO_NOTHING)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "beneficiaries"