# Generated by Django 2.2.7 on 2019-11-30 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_bovid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bovid',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bovid',
            name='date_of_death',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bovid',
            name='date_of_purchase',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bovid',
            name='date_sold',
            field=models.DateField(blank=True, null=True),
        ),
    ]
