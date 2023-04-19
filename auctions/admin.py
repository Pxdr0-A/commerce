from django.contrib import admin
from .models import User, AuctionType, Auction, Listing, Bid, ListingComment

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionType)
admin.site.register(Auction)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(ListingComment)
