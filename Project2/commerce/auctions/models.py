from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listing", default=None)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=150)
    category_choices = [('Electronic', 'electronic'), ('Toys', 'toys'), ('Home', 'home'), ('Fashion', 'fashion'), ('Other', 'other')]
    category = models.CharField(max_length=10, choices=category_choices, default='Other')
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField(blank=True)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid", default=None)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_bids")
    bid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment", default=None)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.CharField(max_length=150)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wishlist", default=None)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_wishlist")
    is_watchlisted = models.BooleanField(default=False)

