# Generated by Django 4.0.2 on 2022-02-27 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Patient", "0016_alter_treatment_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="treatment",
            name="user",
        ),
    ]
