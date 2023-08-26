from random import randint
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'label':'content', 'initial':'content', "rows":1, "cols":1}))

class newArticleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'label':'title', 'initial':'title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'label':'content', 'initial':'content', "rows":1, "cols":1}))

from . import util
def index(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
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
    entry_html = markdown2.markdown(util.get_entry(entry_name))
    if not util.get_entry(entry_name):
        return render(request, "encyclopedia/notfound.html", {
            "page_name": page_name,
            "random_article": random_article,
        })
    else: #if found an article, render that page's article
        return render(request, "encyclopedia/page.html", {
            "entry": util.get_entry(entry_name),
            "random_article": random_article,
            "content": entry_html, 
            "page_name": page_name,
        })

def new_page(request):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]

    if request.method == "POST":
        has_article = False
        form = newArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if (title not in util.list_entries()):
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("page", kwargs={"page_name": title}))
            else:
                has_article = True
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "random_article": random_article,
                    "has_article": has_article,
                })
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "random_article": random_article,
            })
    
    return render(request, "encyclopedia/new_page.html", {
        "form": newArticleForm(),
        "random_article": random_article,
    })

def edit_page(request, article_name):
    random_article = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    entry_name = next((entry for entry in util.list_entries() if entry.lower() == article_name), None)
    article = util.get_entry(entry_name)

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(entry_name, content)
            return HttpResponseRedirect(reverse("page", kwargs={"page_name": article_name}))
    else:
        content = EditForm(initial={'content': article})
        return render(request, "encyclopedia/edit_page.html", {
                "random_article": random_article,
                "content": content,
                "entry_name": entry_name,
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
            return HttpResponseRedirect(reverse("page", kwargs={"page_name": page_name}))
    
    return render(request, "encyclopedia/search_results.html", {
        "random_article": random_article,
    })