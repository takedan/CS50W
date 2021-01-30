
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.allposts, name="allposts"),
    path("allposts1", views.allposts1, name="allposts1"),
    path("fetch_posts", views.fetch_posts, name="fetch_posts"),
    path("add_like", views.add_like, name="add_like"),
    path("<str:username>", views.username , name="user"),
]
