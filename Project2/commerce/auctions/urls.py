from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("search_listing", views.search_listing, name="search_listing"),
    path("listing/<str:listing_title>", views.listing, name="listing"),
    path("bid/<str:listing_title>", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
]
