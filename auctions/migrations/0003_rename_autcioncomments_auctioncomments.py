# Generated by Django 4.1.6 on 2023-02-16 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctions_listings_listingcomments_bids_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AutcionComments',
            new_name='AuctionComments',
        ),
    ]
