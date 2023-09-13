from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def bid_value_validator(value):
    bids = Bid.objects.all()
    bids_values = [value for value in bids.bid]
    if (value <= max(bids_values)):
        raise ValidationError(
            f"the bid ${value} must be higher than the highest bid: ${max(bids_values)}"
        )

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listing", default=None)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=150)
    # category choices
    category_choices = [('Electronic', 'electronic'), ('Toys', 'toys'), ('Home', 'home'), ('Fashion', 'fashion'), ('Other', 'other')]
    category = models.CharField(max_length=10, choices=category_choices, default='Other')
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField()
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid", default=None)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_bids")
    bid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, validators=[bid_value_validator])

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment", default=None)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.CharField(max_length=150)

