# Generated by Django 4.0.2 on 2022-02-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Facility", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facility",
            name="address",
            field=models.TimeField(),
        ),
    ]
