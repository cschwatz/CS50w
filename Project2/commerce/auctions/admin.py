from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)