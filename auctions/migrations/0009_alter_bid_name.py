# Generated by Django 4.1.6 on 2023-03-13 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='name',
            field=models.CharField(default='Unsigned', max_length=64),
        ),
    ]
