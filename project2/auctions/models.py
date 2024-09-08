from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db import models

class Listing(models.Model):
  
    name=models.CharField(max_length=32)
    price=models.FloatField()
    created_at=models.DateField(default=timezone.now)
    description = models.CharField(null=True, max_length=300)
    category=models.CharField(max_length=64) 
    picture = models.ImageField(upload_to="auctions/static/auction/images/",blank=True, null=True)
    active=models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
class Bid(models.Model):
    bid_price=models.FloatField()
    created_at=models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='bid_user')

class Comment(models.Model):
    comment=models.CharField(max_length=64)
    created_at=models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name='comments') 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 