# Generated by Django 4.0.2 on 2022-02-23 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0001_initial'),
        ('Facility', '0004_alter_facility_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='ward',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='System.ward'),
        ),
    ]
