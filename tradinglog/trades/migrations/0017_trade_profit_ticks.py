# Generated by Django 2.2.1 on 2019-06-11 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0016_auto_20190611_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='profit_ticks',
            field=models.FloatField(default=0),
        ),
    ]
