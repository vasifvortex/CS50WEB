from django import forms
from .models import *

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ['name','price','description','category','picture']


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['bid_price']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

class WatchlistForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = ['quantity']

   