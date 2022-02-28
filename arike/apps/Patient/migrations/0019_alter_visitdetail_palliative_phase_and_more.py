# Generated by Django 4.0.2 on 2022-02-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0018_treatment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitdetail',
            name='palliative_phase',
            field=models.IntegerField(choices=[(1, 'Stable'), (2, 'Unstable'), (3, 'Deteriorating'), (4, 'Dying')], default=1),
        ),
        migrations.AlterField(
            model_name='visitdetail',
            name='systemic_examination',
            field=models.IntegerField(choices=[(1, 'Cardiovascular'), (2, 'Gastrointestinal'), (3, 'Central nervous system'), (4, 'Respiratory'), (5, 'Genital-urinary')], default=1),
        ),
    ]
