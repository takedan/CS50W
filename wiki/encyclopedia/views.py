from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import markdown

from . import util


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
