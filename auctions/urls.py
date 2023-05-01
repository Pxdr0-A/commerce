from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # login
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # views
    path("view/<int:id_type>", views.auction_type, name="auction_type"),
    path("view/<int:id_type>/<int:id_auction>", views.auction, name="auction"),
    path("view/<int:id_type>/<int:id_auction>/<int:id_listing>", views.listing, name="listing"),
    # add elements
    path("add/type", views.add_type, name="add_type"),
    path("add/auction/<int:id_type>", views.add_auction, name="add_auction"),
    path("add/auction/<int:id_type>/<int:id_auction>", views.add_listing, name="add_listing"),
    path("add/watchlist/<int:id_type>/<int:id_auction>/<int:id_listing>",
         views.add_to_watchlist,
         name="add_to_watchlist"),
    path("remove/watchlist/<int:id_type>/<int:id_auction>/<int:id_listing>",
         views.remove_from_watchlist,
         name="remove_from_watchlist"),
    path("add/bid/<int:id_type>/<int:id_auction>/<int:id_listing>", views.add_bid, name="add_bid"),
    path("add/comment/<int:id_type>/<int:id_auction>/<int:id_listing>",
         views.add_listing_comment,
         name="add_listing_comment")


]
