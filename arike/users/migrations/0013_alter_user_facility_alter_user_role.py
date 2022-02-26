# Generated by Django 4.0.2 on 2022-02-25 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Facility', '0005_alter_facility_ward'),
        ('users', '0012_alter_user_facility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='facility',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='Facility.facility', verbose_name='Assign Facility'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(2, 'Doctor'), (3, 'Primary Nurse'), (4, 'Secondary Nurse')], default=4, verbose_name='User Role'),
        ),
    ]
