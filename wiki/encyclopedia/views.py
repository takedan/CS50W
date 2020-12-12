from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from django import forms
from . import util
import random

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if util.get_entry(name):
            return wiki(request, name)
        entry_list = util.list_entries()
        list = []
        for entry in entry_list:
            if entry.upper().find(name.upper()) >=0:
                list.append(entry)
        if len(list)>0:
            return render(request, "encyclopedia/index.html", {
                "entries": list
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "name": name,
                "content": "Not found"
            })
    else:   
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def wiki(request, name):
    if not util.get_entry(name):
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "content": "Not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "content": markdown(util.get_entry(name))
        })

class NewPageForm(forms.Form):
    page=forms.CharField(label='Page Title')
    content=forms.CharField(widget=forms.Textarea(
        attrs={
            'style': 'height: 10em;'
        }
    ))

def add_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        html_caller  = request.POST.get('html_caller')
        if form.is_valid():
            page = form.cleaned_data['page']
            content = form.cleaned_data['content']
            if not util.get_entry(page):
                util.save_entry(page, content)
                return HttpResponseRedirect(reverse('encyclopedia:index'))
            else:
                if html_caller == "edit_page":
                    util.save_entry(page, content)
                    return HttpResponseRedirect(reverse('encyclopedia:index'))                    
                else:
                    return HttpResponse('pagina ja existe')
        else:
            return HttpResponse('invalid form')
    else:
        return render(request, "encyclopedia/add_page.html", {
            "form": NewPageForm()
        })

def edit_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        content = util.get_entry(name)
        form = NewPageForm(initial={'page': name, 'content': content})
        return render(request, 'encyclopedia/edit_page.html', {"form": form})

def random_page(request):
    list = util.list_entries()
    n = len(list)
    r = random.randint(1, n)
    return render(request, 'encyclopedia/entry.html', {'name': list[r-1]})