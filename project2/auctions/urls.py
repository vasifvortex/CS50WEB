from django.urls import path  
from django.urls.conf import include  
from django.conf import settings  
from django.conf.urls.static import static  

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name='create'),
    path('category', views.category, name='category'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('listing/<int:listing_id>/', views.listing, name='listing'),
    path('category/<str:category>', views.listing_category, name='listing_category'),
    path('add_watchlist/<int:listing_id>', views.add_watchlist, name='add_watchlist'),
    path('close/<int:listing_id>', views.close, name='close')
  
   
   
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        



