# Generated by Django 4.2.7 on 2023-12-04 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_username'),
        ('farmers', '0003_remove_farmer_block_remove_farmer_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='added_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='added_by', to='users.user'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='last_edited_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='last_edited_by', to='users.user'),
        ),
    ]
