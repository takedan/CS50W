from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, ItemCategory, CreateList, BidItem, ItemActive, Watchlist

class NewItemForm(forms.ModelForm):
    class Meta:
        model = CreateList
        fields = ('title', 'description', 'price', 'imageurl', 'category')

class NewBidForm(forms.ModelForm):
    class Meta:
        model = BidItem
        fields = ('bid',)

# class NewComment(forms.ModelForm):
#     class Meta:
#         model = Comments
#         fields = ('text',)

def index(request):
    filt = request.GET.get('filtercategory', 'nofilter')

    if filt == "nofilter":
        return render(request, "auctions/index.html", {
            "items": CreateList.objects.all(),
            "categories": ItemCategory.objects.all()
        })
    else:
        cat = ItemCategory.objects.get(Category=filt)
        filtros = CreateList.objects.filter(category=cat.CategoryID)
        return render(request, "auctions/index.html", {
            "items": filtros,
            "categories": ItemCategory.objects.all()
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

def createlist(request):
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario = request.user
            item.bid=0
            item.save()
            f = ItemActive.objects.create(item=CreateList.objects.get(title=item.title), active=True)
            f.save()
            return redirect("index")
    return render(request, "auctions/createlist.html", {
        "form": NewItemForm()
    })

def item(request, itemid, message=""):

    #inicializa
    i = CreateList.objects.get(id=itemid)
    bids = BidItem.objects.filter(item=i)
    itemactive = ItemActive.objects.get(item=CreateList(id=itemid)).active

    #pega comentarios
    # cs = Comments.objects.filter(item=CreateList(id=itemid))
    # if len(cs)<=0:
    #     cs = "sem comentarios"

    #verifica se esta na watchlist
    if request.user.is_authenticated:
        watch = Watchlist.objects.get(user=request.user)
        for it in watch.items.all():
            if it.title == i.title:
                watching = True
                break
            else:
                watching = False
    else:
        watching = False

    n_bids = len(bids)
    if n_bids>0:
        max = bids.order_by('-bid')[0]
        #verifica se o bid atual e o seu
        if max.usuario == request.user:
            bid_atual = True
        else:
            bid_atual = False
        #ajusta preco p/ max bid
        maximo= max.bid    
        #verifica quem ganhou
        if itemactive == True:
            winner = ""
        else:
            winner = max.usuario               
    else:
        maximo = i.price
        bid_atual = False
        winner=""
        message="Nao há bids nesse item"

    #verifica se vc e o dono do item
    if request.user == i.usuario:
        owner = True
    else:
        owner = False

    return render(request, "auctions/item.html", {
        "item": i,
        "form": NewBidForm(initial={'bid': maximo}),
        "nbids": n_bids,
        "bidatual": bid_atual,
        "message": message,
        "owner": owner,
        "itemactive": itemactive,
        "winner": winner,
        "watching": watching,
        # "cs": cs,
        # "formcom": NewComment()
    })

@login_required
def placebid(request):
    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            n_bids = len(BidItem.objects.filter(item=CreateList(id=request.POST['item'])))
            if n_bids>0: 
                max = BidItem.objects.filter(item=CreateList(id=request.POST['item'])).order_by('-bid')[0]
                maximo = max.bid
            else:
                maximo = 0
            bid = form.save(commit=False)
            if bid.bid > maximo:
                #save bid
                bid.usuario = request.user
                bid.item = CreateList(id=request.POST['item'])
                bid.save()
                a = CreateList.objects.get(id=request.POST['item'])
                a.bid = bid.bid
                a.save()
                return HttpResponseRedirect(reverse("item", kwargs={'itemid': request.POST['item']}))
            else:
                return HttpResponse('Seu bid nao foi aceito pois e menor que o valor atual')
        else:
            return HttpResponse('formulario invalido')

@login_required
def closeitem(request):
    f = ItemActive()
    f.item = CreateList(id=request.POST['item'])
    f.active = False
    f.save()
    return HttpResponseRedirect(reverse("item", kwargs={'itemid': request.POST['item']}))

def listbids(request):
    itemid = request.POST['item']
    bids = BidItem.objects.filter(item=CreateList(id=itemid))
    return render(request, "auctions/listbids.html", {
        "bids": bids
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        f = Watchlist.objects.get(user=request.user)
        f.items.add(CreateList.objects.get(id=request.POST['item']))
    f = Watchlist(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "items": f.items.all()
    })

@login_required
def delwatchlist(request):
    if request.method == "POST":
        f = Watchlist.objects.get(user=request.user)
        f.items.remove(CreateList.objects.get(id=request.POST['item']))
    f = Watchlist(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "items": f.items.all()
    })

@login_required
def addcomment(request):
    return HttpResponse(request.user)
    # if request.method == "POST":
    #     f = NewComment(request.POST)
    #     if f.is_valid():
    #         f.user = request.user
    #         f.item = CreateList.objects.get(id=request.POST['item'])
    #         return HttpResponse(request.user)
    #         c = f.save(commit=False)
    #         return HttpResponse(c)
    #         f.save()
    # return HttpResponseRedirect(reverse("item", kwargs={'itemid': request.POST['item']}))