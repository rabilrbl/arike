# Generated by Django 4.0.2 on 2022-02-26 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0008_patientdisease_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disease',
            old_name='icd_code',
            new_name='icds_code',
        ),
    ]
