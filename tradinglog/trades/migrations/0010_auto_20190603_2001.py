# Generated by Django 2.2.1 on 2019-06-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0009_trade_result'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trade',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='trade',
            name='close_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Open'), (2, 'Closed')], default=1),
        ),
    ]
