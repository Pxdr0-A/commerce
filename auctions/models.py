from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionType(models.Model):
    type_name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return f"{self.type_name}"

class Auction(models.Model):
    auction_name = models.CharField(max_length=64)
    auction_type = models.ForeignKey(AuctionType, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField()
    
    def __str__(self):
        return f"{self.auction_name} of type {self.auction_type}"

class Listing(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="listings")
    listing = models.CharField(max_length=64)
    description = models.TextField()
    active = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.listing} in auction {self.auction}"

class Bid(models.Model):
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self) -> str:
        return f"{self.bid} on listing {self.product}"

class ListingComment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self) -> str:
        return f"Comment on listing {self.listing}"
