# Generated by Django 2.2.1 on 2019-06-03 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0006_auto_20190603_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='close_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
