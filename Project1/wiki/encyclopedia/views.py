from random import randint
from django.shortcuts import render

from . import util
def index(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random_article": random_article,
    })

def css(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/css.html", {
        "entry": util.get_entry("CSS"),
        "random_article": random_article,
    })

def django(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/django.html", {
        "entry": util.get_entry("Django"),
        "random_article": random_article,
    })

def git(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/git.html", {
        "entry": util.get_entry("Git"),
        "random_article": random_article,
    })

def html(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/html.html", {
        "entry": util.get_entry("HTML"),
        "random_article": random_article,
    })

def python(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/python.html", {
        "entry": util.get_entry("Python"),
        "random_article": random_article,
    })

def page(request, page_name):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]

    if page_name == "" or not page_name or page_name == '':
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random_article": random_article,
    })

    #creates a generator and returns (with the 'next' function) the first occurence in the conditional, else returns a default value (None in this case)
    entry_name = next((entry for entry in util.list_entries() if entry.lower() == page_name), None)
    #checks if the name entered at the url directly corresponds to any article that is in 'entries'
    #if article does not exist, renders the 'notfound' page
    if not util.get_entry(entry_name):
        return render(request, "encyclopedia/notfound.html", {
            "page_name": page_name,
            "random_article": random_article,
        })
    else: #if found an article, render that page's article
        return render(request, f"encyclopedia/{page_name}.html", {
            "entry": util.get_entry(entry_name),
            "random_article": random_article,
        })

def search_results(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]

    if request.method == "POST":
        page_name = request.POST.get('q')
        entry_name = next((entry for entry in util.list_entries() if entry.lower() == page_name), None)
        if not util.get_entry(entry_name):
            matching_results = [article for article in util.list_entries() if page_name in article.lower()]
            return render(request, "encyclopedia/search_results.html", {
                "matching_articles": matching_results,
                "random_article": random_article,
            })
        else: #if found an article, render that page's article
            return render(request, f"encyclopedia/{page_name}.html", {
                "entry": util.get_entry(entry_name),
                "random_article": random_article,
            })
    
    return render(request, "encyclopedia/search_results.html", {
        "random_article": random_article,
    })