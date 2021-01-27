from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Post, Follow, Comment

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)

class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

def index(request):
    return render(request, "network/index.html")

def username(request, username):
    user = request.user
    following = Follow.objects.get(user=User.objects.get(username=username)).list.all()
    n_following = following.count()
    followers = Follow.objects.filter(list=user.id)
    n_followers = 0
    return render(request, "network/user.html", {
        "n_following": n_following,
        "following": following,
        "followers": followers,
        "n_followers": n_followers,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
