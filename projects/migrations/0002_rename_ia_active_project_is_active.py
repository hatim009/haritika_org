# Generated by Django 4.2.7 on 2023-12-05 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='ia_active',
            new_name='is_active',
        ),
    ]
