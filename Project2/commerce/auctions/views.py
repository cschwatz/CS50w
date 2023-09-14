from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, AuctionListing, Bid, Comment

class newListingForm(forms.Form):
    listing_name = forms.CharField(widget=forms.TextInput(attrs={'label': 'Listing name', 'initial':'Listing name'}))
    image_url = forms.CharField(widget=forms.TextInput(attrs={'label': 'Image URL'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'label': 'Description'}))
    choices = [('EL', 'electronic'), ('TO', 'toys'), ('HM', 'home'), ('FS', 'fashion'), ('OT', 'other')]
    category = forms.ChoiceField(choices=choices)
    initial_price = forms.DecimalField(widget=forms.NumberInput())

class searchListingForm(forms.Form):
    choices = [('EL', 'electronic'), ('TO', 'toys'), ('HM', 'home'), ('FS', 'fashion'), ('OT', 'other')]
    category_to_search = forms.ChoiceField(choices=choices)

class bidForm(forms.Form):
    value = forms.DecimalField(widget=forms.NumberInput(attrs={'label': 'Bid'}), min_value=0)


def index(request):
    active_auctions = AuctionListing.objects.all() # get all active auctions (still have to work on the "active" aspect)
    listings_with_bid = [] # list of tuples that have a listing and their respective highest bid
    for listing in active_auctions:
        try: # see if there are bids for a given listing
            highest_bid = Bid.objects.filter(listing=listing)
            highest_bid = highest_bid.order_by('-bid')[0].bid
        except IndexError: #if there are no bids, the highest bid is the initial value
            highest_bid = listing.value
        listings_with_bid.append((listing, highest_bid))
    
    return render(request, "auctions/index.html", {
        "listings": listings_with_bid,
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


def listing(request, listing_title):
    listing_to_view = AuctionListing.objects.get(title=listing_title)
    try:
        highest_bid = Bid.objects.filter(listing=listing_to_view) #gets all bids for the listing
        highest_bid = highest_bid.order_by('bid')[0].bid #order them from highest bid to lowest and fetches the first one (highest)
    except IndexError: #if there are no bids, it will throw an index error
        highest_bid = listing_to_view.value
    user_can_bid = False
    user_can_close_listing = False
    if (listing_to_view.user.username != request.user.username): # check if logged user is not the user who created the current listing, since they shouldn't bid on their own listing
        user_can_bid = True
    else:
        user_can_close_listing = True
    return render(request, "auctions/listing.html", {
        "listing_to_view": listing_to_view,
        "highest_bid": highest_bid,
        "can_bid": user_can_bid,
        "can_close": user_can_close_listing,
    })

@login_required
def create_listing(request):
    is_post = False
    if request.method == "POST":
        is_post = True
        form = newListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['listing_name']
            image_url = form.cleaned_data['image_url']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            initial_price = form.cleaned_data['initial_price']
            user = User.objects.get(username=request.user.username)
            listing = AuctionListing(user=user, title=title, description=description, category=category, image=image_url, value=initial_price)
            listing.save()
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_title": title}))

    return render(request, "auctions/create_listing.html", {
        "form": newListingForm(),
        "is_post": is_post,
    })

def search_listing(request):
    if request.method == "POST":
        form = searchListingForm(request.POST)
        if form.is_valid():
            test = form.cleaned_data['category_to_search']
            matching_listings = AuctionListing.objects.filter(category=form.cleaned_data['category_to_search'])
            listings_with_bid = []
            for match in matching_listings:
                try: # see if there are bids for a given listing
                    highest_bid = Bid.objects.filter(listing=match)
                    highest_bid = highest_bid.order_by('bid')[0].bid
                except IndexError: #if there are no bids, the highest bid is the initial value
                    highest_bid = match.value
                listings_with_bid.append((match, highest_bid))
            return render(request, "auctions/search_listing.html", {
                "form": searchListingForm(),
                "matches": listings_with_bid,
            })

    return render(request, "auctions/search_listing.html", {
        "form": searchListingForm(),
    })

@login_required
def bid(request, listing_title):
    listing = AuctionListing.objects.get(title=listing_title)
    try:
        highest_bid = Bid.objects.filter(listing=listing) #gets all bids for the listing
        highest_bid = highest_bid.order_by('bid')[0].bid #order them from highest bid to lowest and fetches the first one (highest)
    except IndexError: #if there are no bids, it will throw an index error
        highest_bid = listing.value
    form = bidForm()

    if request.method == "POST":
        form = bidForm(request.POST)
        if form.is_valid():
            new_bid = form.cleaned_data['value']
            listing_user = listing.user
            current_bid = highest_bid
            if new_bid <= current_bid:
                bid_message = "Your bid must be greater than the current highest bid"
                return render(request, "auctions/bid.html", {
                    "form": form,
                    "listing": listing,
                    "current_bid": current_bid,
                    "listing_user": listing_user,
                    "error_message": bid_message,
                })
            else:
                bid_to_save = Bid(user=request.user, listing=listing, bid=new_bid)
                bid_to_save.save()
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_title": listing_title}))
    else:        
        return render(request, "auctions/bid.html", {
            "form": form,
            "listing": listing,
            "highest_bid": highest_bid,
        })