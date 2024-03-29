# Generated by Django 4.0.2 on 2022-02-24 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Facility", "0005_alter_facility_ward"),
        ("System", "0001_initial"),
        ("users", "0006_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="district",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="System.district",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="facility",
            field=models.ForeignKey(
                default="",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="Facility.facility",
            ),
        ),
    ]
