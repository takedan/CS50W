from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime
from time import sleep

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
    n_followers = followers.count()
    return render(request, "network/user.html", {
        "n_following": n_following,
        "following": following,
        "followers": followers,
        "n_followers": n_followers,
    })

def allposts(request):
    #create object using django forms
    if request.method == "POST":
        f = NewPost(request.POST)
        if f.is_valid():
            form = f.save(commit=False)
            form.datecreation = datetime.now()
            form.user_id = User.objects.get(username=request.user.username).id
            form.save()
            return render(request, "network/allposts.html", {
                "message": "Postado!",
                "classe": "alert alert-primary",
                "form": NewPost()
            })
        else:
            return render(request, "network/allposts.html", {
                "message": "ERRO",
                "classe": "alert alert-danger",
                "form": NewPost()
            })
    else:
        return render(request, "network/allposts.html", {
            "form": NewPost()
        })

def allposts1(request):
    #create object
    if request.method == "POST":
        form = Post(text = request.POST['text_newpost'], datecreation=datetime.now(), user_id  = User.objects.get(username=request.user.username).id)
        try:
            form.save()
            return render(request, "network/allposts1.html", {
                "message": "Postado!",
                "classe": "alert alert-primary",
                "form": NewPost()
            })
        except:
            return render(request, "network/allposts1.html", {
                "message": "ERRO",
                "classe": "alert alert-danger",
                "form": NewPost()
            })            
    else:
        return render(request, "network/allposts1.html")

def fetch_posts(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start+ 9))

    p = Post.objects.all().order_by('-datecreation')

    header = []
    content = []
    data = []
    likes = []
    for i in p:
        dt_format = i.datecreation.strftime("%d/%m/%Y %H:%M:%S")
        header.append(f"{i.user} {dt_format}")
        content.append(f"{i.text}")
        data.append(f"{i.id}")
        likes.append(f"{i.likes}")
    sleep(1)

    return JsonResponse({
        "posts": data,
        "h": header,
        "c": content,
        "l": likes,
    })    

def add_like(request):
    if request.method == "GET":
        post_id = request.GET.get('post_id')
        p = Post.objects.get(id=post_id)
        p.likes = p.likes+1
        p.save()
        return HttpResponse(p.likes)
    else:
        return HttpResponse("post")

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
