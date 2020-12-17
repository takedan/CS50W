from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.createlist, name="createlist"),
    path("item/<int:itemid>", views.item, name="item"),
    path("placebid", views.placebid, name="placebid"),
    path('closeitem', views.closeitem, name="closeitem"),
    path('listbids', views.listbids, name='listbids'),
    path('watchlist', views.watchlist, name="watchlist"),
    path('delwatchlist', views.delwatchlist, name="delwatchlist")    
]