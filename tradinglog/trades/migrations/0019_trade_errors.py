# Generated by Django 2.2.1 on 2019-06-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0018_tradeerrors'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='errors',
            field=models.ManyToManyField(to='trades.TradeErrors'),
        ),
    ]
