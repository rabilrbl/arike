# Generated by Django 4.0.2 on 2022-02-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'District Admin'), (2, 'Doctor'), (3, 'Primary Nurse'), (4, 'Secondary Nurse')], default=2),
        ),
    ]
