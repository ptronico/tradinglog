# Generated by Django 2.2.1 on 2019-06-03 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0010_auto_20190603_2001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trade',
            options={'ordering': ('-close_date', '-id')},
        ),
    ]