from django.shortcuts import render, redirect
import markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_view(request, title):
    entry_content = util.get_entry(title)

    if entry_content:
        html_content = markdown.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {"title": title, "content": entry_content})
    else:
        return render(request, "encyclopedia/error.html", {"error_message": "Entry not found"}) 


def search_view(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    
    direct_match = [entry for entry in entries if query.lower() == entry.lower()]

    if direct_match:
        # If a direct match is found, redirect to the corresponding entry page
        return redirect('entry_view', title=direct_match[0])
    else:
        # If no direct match is found, perform the regular search
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {"query": query, "results": results})

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def new_page_view(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Save the new entry using the save_entry function from util.py
            util.save_entry(title, content)
            # Redirect to the newly created entry's page
            return redirect("entry_view", title=title)
    else:
        form = NewPageForm()
    
    return render(request, "encyclopedia/new_page.html", {"form": form})

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def edit_page_view(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return redirect("entry_view", title=title)

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry_view", title=title)
    else:
        form = EditPageForm(initial={"content": entry_content})

    return render(request, "encyclopedia/edit_page.html", {"form": form, "entry_title": title, "entry_content": entry_content})

def random_page_view(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect("entry_view", title=random_title)