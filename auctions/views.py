from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, AuctionType, Listing, ListingComment, Bid
from .my_forms import AddBid, AddCommentForm, AddAuction, AddListing, AddType


def index(request):
    data = AuctionType.objects.all()
    types = []
    for obj in data:
        types.append((
            obj.id, obj.type_name,
            obj.description,
            len(obj.auctions.filter(active=True))
        ))

    watch_list = []
    if request.user.is_authenticated:
        watch_list = request.user.watch_list.all()

    return render(request, "auctions/index.html", {
        "types": types,
        "add_type_form": AddType(),
        "watch_list": watch_list
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
    # ADD A START LISTING OPTION
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
        "auctions": auctions,
        "add_auction_form": AddAuction(),
        "add_listing_form": AddListing()
    })


def auction(request, id_type, id_auction):
    auction_type_obj = AuctionType.objects.filter(id=id_type).first()
    auction_obj = auction_type_obj.auctions.filter(id=id_auction).first()
    auction_info = [
        id_type,
        id_auction,
        auction_type_obj.type_name,
        auction_obj.auction_name
    ]

    active_listings = auction_obj.listings.filter(active=True)
    listings = []
    for obj in active_listings:
        listings.append((
            obj.id, obj.listing, obj.description, len(obj.bids.all()), obj.url
        ))
    return render(request, "auctions/auction.html", {
        "auction_info": auction_info,
        "listings": listings,
        "add_listing_form": AddListing(),
        "add_bid_form": AddBid(),
    })


def listing(request, id_type, id_auction, id_listing):
    auction_type_obj = AuctionType.objects.filter(id=id_type).first()
    auction_obj = auction_type_obj.auctions.filter(id=id_auction).first()
    listing_obj = auction_obj.listings.filter(id=id_listing).first()
    comments = listing_obj.comments.all()
    listing_info = [
        id_type,
        id_auction,
        id_listing,
        auction_type_obj.type_name,
        auction_obj.auction_name,
        listing_obj.listing,
        listing_obj.description,
        listing_obj.url,
        listing_obj.author
    ]
    watch_list = request.user.watch_list.all()
    if Listing.objects.get(id=id_listing) in watch_list:
        listing_in_watchlist = True
    else:
        listing_in_watchlist = False

    all_bids = listing_obj.bids.all().order_by("-bid")
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
        "add_comment_form": AddCommentForm(),
        "listing_in_watchlist": listing_in_watchlist
    })


def add_type(request):
    if request.method == "POST":
        form = AddType(request.POST)

        if form.is_valid():
            type_obj = AuctionType(
                type_name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
            )
            type_obj.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect(reverse("index"))


def add_auction(request, id_type):
    if request.method == "POST":
        form = AddAuction(request.POST)

        if form.is_valid():
            auction_obj = Auction(
                auction_name=form.cleaned_data["name"],
                auction_type=AuctionType.objects.filter(id=id_type).first(),
                active=form.cleaned_data["active"]
            )
            auction_obj.save()

            return HttpResponseRedirect(reverse("auction_type", args=(id_type,)))
        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect(reverse("auction_type", args=(id_type,)))


def add_listing(request, id_type, id_auction):
    if request.method == "POST":
        form = AddListing(request.POST)

        if form.is_valid():
            listing_obj = Listing(
                auction=Auction.objects.filter(id=id_auction).first(),
                author=request.user,
                listing=form.cleaned_data["listing"],
                description=form.cleaned_data["description"],
                url=form.cleaned_data["url"],
                active=form.cleaned_data["active"]
            )
            listing_obj.save()

            return HttpResponseRedirect(reverse("auction", args=(id_type, id_auction)))
        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect(reverse("auction", args=(id_type, id_auction)))


def add_bid(request, id_type, id_auction, id_listing):
    if request.method == "POST":
        form = AddBid(request.POST)

        if form.is_valid():
            bid = form.cleaned_data["bid"]

            auction_type_obj = AuctionType.objects.filter(id=id_type).first()
            auction_obj = auction_type_obj.auctions.filter(id=id_auction).first()
            listing_obj = auction_obj.listings.filter(id=id_listing).first()
            all_bids = listing_obj.bids.all().order_by("-bid")
            try:
                current_bid = all_bids.first().bid
            except AttributeError:
                current_bid = 0

            if bid <= current_bid is not None:
                messages.error(request, "The bid needs to be higher than the current one.")
                return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))

            user = request.user
            listing_obj = Listing.objects.get(id=id_listing)
            name = User.objects.get(username=user)
            bid_obj = Bid(product=listing_obj, name=name, bid=bid)
            bid_obj.save()

            return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))
        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))


def add_listing_comment(request, id_type, id_auction, id_listing):
    if request.method == "POST":
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.cleaned_data["comment"]
            user = request.user

            listing_obj = Listing.objects.get(id=id_listing)
            name = User.objects.get(username=user)
            comment_obj = ListingComment(listing=listing_obj, name=name, comment=comment)
            comment_obj.save()

            return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))


def add_to_watchlist(request, id_type, id_auction, id_listing):
    if request.method == "POST":
        listing_obj = Listing.objects.get(id=id_listing)
        listing_obj.watch_list.add(request.user)
        messages.info(request, "Successfully added to your watchlist.")

    return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))


def remove_from_watchlist(request, id_type, id_auction, id_listing):
    if request.method == "POST":
        listing_obj = Listing.objects.get(id=id_listing)
        listing_obj.watch_list.remove(request.user)
        messages.info(request, "Listing removed from your watchlist.")

    return HttpResponseRedirect(reverse("listing", args=(id_type, id_auction, id_listing)))
