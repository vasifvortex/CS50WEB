from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.http import HttpResponse
import random
from django import forms


markdowner = Markdown()
class NewForm(forms.Form):
    name=forms.CharField(label="name")
    content = forms.CharField(widget=forms.Textarea, label="content")

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request,title):
    try:
        return render(request, "encyclopedia/entry.html", {
        "name":  title,
        
        "content": markdowner.convert(util.get_entry(title))
        })
    except:
        return render(request, "encyclopedia/entry.html", {
        "name":  title,
        
        "content": None
        })
    

def search(request):
    query=request.GET.get('q')
    try:
        return render(request, "encyclopedia/entry.html", {
        "name":  query,
        
        "content": markdowner.convert(util.get_entry(query))
        })
    except:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "name":query
    })


def randomly(request):
    r=random.choice(util.list_entries())
    try:
        return render(request, "encyclopedia/entry.html", {
        "name":  r,
        
        "content": markdowner.convert(util.get_entry(r))
        })
    except:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "name":r
    })


def new(request):
     return render(request, "encyclopedia/new.html")


def add(request):
    if request.method == "POST":
        form=NewForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data['content']
            name=form.cleaned_data["name"]
            
            if name not in util.list_entries():
                util.save_entry(name,content)
                return render(request, "encyclopedia/entry.html", {
                "name":name,
                "content": markdowner.convert(util.get_entry(name))})
            else:
                return render(request, "encyclopedia/entry.html", {
                "name":name,
                "content": markdowner.convert("<h1>Requested page already exist.</h1>")
    })
        
def newedit(request,title):
     return render(request, "encyclopedia/edit.html",{
         "name":title,
         "content": markdowner.convert(util.get_entry(title))
     })

def edit(request,title):
    if request.method == "POST":
        form=EditForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data['content']
            util.save_entry(title,content)
            return render(request, "encyclopedia/entry.html", {
             "name":title,   
             "content": markdowner.convert(content)})
        
    
    
