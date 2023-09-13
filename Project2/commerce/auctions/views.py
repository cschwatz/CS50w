from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, AuctionListing

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

class checkUserForm(forms.Form):
    pass

def index(request):
    active_auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "active_auctions": active_auctions,
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
    return render(request, "auctions/listing.html", {
        "listing_to_view": listing_to_view,
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
            return render(request, "auctions/search_listing.html", {
                "form": searchListingForm(),
                "matching_listings": matching_listings,
                "test": test,
            })

    return render(request, "auctions/search_listing.html", {
        "form": searchListingForm(),
    })

def bid(request, listing_title):
    pass