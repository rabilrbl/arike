# Generated by Django 4.0.2 on 2022-03-01 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0021_alter_visitdetail_mouth_hygiene_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitdetail',
            name='patient_at_peace',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]
