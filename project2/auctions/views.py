from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404        
from django.contrib import messages

def index(request):
    if request.method == 'GET':
        listings = Listing.objects.all()
        return render(request, 'auctions/index.html',
                       {'list_images': listings}) 


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
    
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *


@login_required
def create(request):

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        listings = Listing.objects.all()
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            messages.success(request, "Successfully uploaded")
            return render(request,'auctions/index.html', {'list_images': listings}) 
    else:
        form = ListingForm()
    return render(request, 'auctions/create.html', {'form': form})

def category(request):
    if request.method == 'GET':
        a={}
        listings = Listing.objects.all()
        for i in range(len(listings)):
            if listings[i].active:
                if listings[i].category not in a.values():
                    a.update({i: listings[i].category})        
        return render(request, 'auctions/categories.html',
                       {'categories': a}) 

@login_required
def add_watchlist(request,listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=listing_id)
        if Watchlist.objects.filter(user=request.user, listing=listing).exists():
             watchlist_items = Watchlist.objects.filter(user=request.user)
             if Watchlist.objects.filter(id=listing_id).exists():
                Watchlist.objects.filter(user=request.user, listing=listing).delete()
                return redirect('watchlist') 
             else:
                return render(request,'auctions/watchlist.html',{'watchlist_items': watchlist_items})
        Watchlist.objects.create(user=request.user, listing=listing)
        return redirect('watchlist') 
    
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})

def layout(request):
    if request.user.is_authenticated:
        count = Watchlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'count': count}
    
def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    comments = listing.comments.all().order_by('-created_at')
    bids= listing.bids.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            formc = CommentForm(request.POST)
            formb= BidForm(request.POST)
            if formc.is_valid():
                new_comment = formc.save(commit=False)
                new_comment.user = request.user
                new_comment.listing = listing
                new_comment.save()
                return redirect('listing', listing_id=listing.id)
            if formb.is_valid():
                new_bid = formb.save(commit=False)
                if new_bid.bid_price >=listing.price:
                    listing.price=new_bid.bid_price
                    listing.save()
                    new_bid.user = request.user
                    new_bid.listing = listing
                    new_bid.save()
                    return redirect('listing', listing_id=listing.id)
                else:
                    return render(request,'auctions/listing.html', {
        'listing': listing,
        'comments': comments,
        'bids':bids,
        'formc': formc,
        'formb': formb,
        'message':"Bid must be higher!"
    })
              
        else:
            return redirect('login')
        
    else:
        formc = CommentForm()
        formb = BidForm()

    
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'comments': comments,
        'bids':bids,
        'formc': formc,
        'formb': formb
    })

 
def listing_category(request,category):
    if request.method == 'GET':
        a={}
        listings = Listing.objects.all()
        for i in range(len(listings)):
            if listings[i].category==category:
                a.update({listings[i]: listings[i].category})     
        return render(request, 'auctions/index.html',
                       {'list_images': a}) 
    
def close(request,listing_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            listing = get_object_or_404(Listing, id=listing_id)
            listing.active=False
            listing.save()
            
            
            return render(request,'auctions/listing.html', {
        'listing': listing,
     
    })
