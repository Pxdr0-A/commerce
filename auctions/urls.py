from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("view/<int:id_type>", views.auction_type, name="auction_type"),
    path("view/<int:id_type>/<int:id_auction>", views.auction, name="auction"),
    path("view/<int:id_type>/<int:id_auction>/<int:id_listing>", views.listing, name="listing"),
    path("add/comment/<int:id_type>/<int:id_auction>/<int:id_listing>", views.add_listing_comment, name="add_listing_comment"),
    path("add/bid/<int:id_type>/<int:id_auction>/<int:id_listing>", views.add_bid, name="add_bid")
]
