# Generated by Django 4.1.6 on 2023-03-13 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='name',
        ),
    ]
