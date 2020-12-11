from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import markdown

from . import util


def index(request):
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
        #return HttpResponse(markdown(util.get_entry(name)))