from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, AuctionType, Auction, Listing, ListingComment, Bid
from .my_forms import AddBid, AddCommentForm

def index(request):
    data = AuctionType.objects.all()
    types = []
    for obj in data:
        types.append((
            obj.id, obj.type_name, 
            obj.description, 
            len(obj.auctions.filter(active=True))
        ))

    return render(request, "auctions/index.html", {
        "types": types
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def auction_type(request, id_type):
    data = AuctionType.objects.filter(id=id_type).first()
    type_name = data.type_name
    description = data.description
    active_auctions = data.auctions.filter(active=True)
    auctions = []
    for obj in active_auctions:
        auctions.append((
            obj.id, obj.auction_name, len(obj.listings.filter(active=True))
        ))

    return render(request, "auctions/type.html", {
        "type_info": [id_type, type_name, description],
        "auctions": auctions
    })

def auction(request, id_type, id_auction):
    auction_type = AuctionType.objects.filter(id=id_type).first()
    auction = auction_type.auctions.filter(id=id_auction).first()
    auction_info = [id_type, id_auction, auction_type.type_name, auction.auction_name]

    active_listings = auction.listings.filter(active=True)
    listings = []
    for obj in active_listings:
        listings.append((
            obj.id, obj.listing, obj.description, len(obj.bids.all())
        ))
    return render(request, "auctions/auction.html", {
        "auction_info": auction_info,
        "listings": listings,
        "add_bid_form": AddBid(),
    })

def listing(request, id_type, id_auction, id_listing):
    auction_type = AuctionType.objects.filter(id=id_type).first()
    auction = auction_type.auctions.filter(id=id_auction).first()
    listing = auction.listings.filter(id=id_listing).first()
    comments = listing.comments.all()
    listing_info = [id_type, id_auction, id_listing, auction_type.type_name, auction.auction_name, listing.listing, listing.description]

    all_bids = listing.bids.all().order_by("-bid")
    bids = []
    for obj in all_bids:
        bids.append((
            obj.bid, obj.name
        ))

    return render(request, "auctions/listing.html", {
        "bids": bids,
        "listing_info": listing_info,
        "comments": comments.order_by("-id"),
        "add_bid_form": AddBid(),
        "add_comment_form": AddCommentForm()
    })

def add_bid(request, id_type, id_auction, id_listing):
    if request.method == "POST":
        form = AddBid(request.POST)

        if form.is_valid():
            bid = form.cleaned_data["bid"]
            
            auction_type = AuctionType.objects.filter(id=id_type).first()
            auction = auction_type.auctions.filter(id=id_auction).first()
            listing = auction.listings.filter(id=id_listing).first()
            all_bids = listing.bids.all().order_by("-bid")
            try:
                current_bid = all_bids.first().bid
            except AttributeError:
                current_bid = 0

            if current_bid >= bid and current_bid != None:
                messages.error(request, "The bid needs to be higher than the current one.")
                return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))

            user = request.user
            listing = Listing.objects.get(id=id_listing)
            name = User.objects.get(username=user)
            bid_obj = Bid(product=listing, name=name, bid=bid)
            bid_obj.save()

            return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))
        else:
            messages.error(request, "Form is not valid.")
        
def add_listing_comment(request, id_type, id_auction, id_listing):
    if request.method == "POST":
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.cleaned_data["comment"]
            user = request.user

            listing = Listing.objects.get(id=id_listing)
            name = User.objects.get(username=user)
            comment_obj = ListingComment(listing=listing, name=name, comment=comment)
            comment_obj.save()

            return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))