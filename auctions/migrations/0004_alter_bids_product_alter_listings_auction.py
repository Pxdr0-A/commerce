# Generated by Django 4.1.6 on 2023-03-04 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_autcioncomments_auctioncomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listings'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.auctions'),
        ),
    ]
