from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)


class AuctionType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return f"{self.type_name}"


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    auction_name = models.CharField(max_length=64)
    auction_type = models.ForeignKey(AuctionType, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField()

    def __str__(self):
        return f"{self.auction_name} of type {self.auction_type}"


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="listings")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default="0")
    watch_list = models.ManyToManyField(User, blank=True, related_name="watch_list")
    listing = models.CharField(max_length=64)
    description = models.TextField()
    url = models.URLField(default="")
    active = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.listing} in auction {self.auction}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self) -> str:
        return f"{self.bid} on listing {self.product}"


class ListingComment(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self) -> str:
        return f"Comment on listing {self.listing}"
