# Generated by Django 2.2.7 on 2019-12-01 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20191130_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bovid',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.Tag'),
        ),
    ]
