from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=150)
    # category choices
    # category_choices = [('EL', 'electronic'), ('TO', 'toys'), ('HM', 'home'), ('FS', 'fashion'), ('OT', 'other')]
    # category = models.CharField(max_length=2, choices=category_choices, default='OT')
    category = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField()
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

# class Bids(models.Model):
#     current_bid = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid")
#     bids = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

# class Comments(models.Model):
#     comment = models.CharField(max_length=150)

