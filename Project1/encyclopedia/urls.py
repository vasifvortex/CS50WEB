from django.urls import path,re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("newedit/<str:title>", views.newedit, name="newedit"),
    re_path(r'^search/.*$',  views.search, name="search"),
    re_path(r'^random/.*$',views.randomly,name="random"),
    re_path(r'^new/.*$',views.new,name="new"),
    re_path(r'^add/.*$',views.add,name='add'),
    path("edit/<str:title>",views.edit,name='edit'),
]
