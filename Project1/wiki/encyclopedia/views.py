from django.shortcuts import render

from . import util

lowercase_names = [entry.lower() for entry in util.list_entries()]

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "lower_entries": lowercase_names,
    })

def css(request):
    return render(request, "encyclopedia/css.html", {
        "entry": util.get_entry("CSS")
    })

def django(request):
    return render(request, "encyclopedia/django.html", {
        "entry": util.get_entry("Django")
    })

def git(request):
    return render(request, "encyclopedia/git.html", {
        "entry": util.get_entry("Git")
    })

def html(request):
    return render(request, "encyclopedia/html.html", {
        "entry": util.get_entry("HTML")
    })

def python(request):
    return render(request, "encyclopedia/python.html", {
        "entry": util.get_entry("Python")
    })