# Generated by Django 4.0.2 on 2022-03-01 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Nurse", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reports",
            name="last_sent",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2022, 3, 1, 0, 0),
                help_text="Choose time",
                null=True,
            ),
        ),
    ]
