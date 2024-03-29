# Generated by Django 4.0.2 on 2022-02-27 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Patient", "0015_alter_treatment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="treatment",
            name="user",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
