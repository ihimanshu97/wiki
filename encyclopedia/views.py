from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from markdown2 import markdown
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def title(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {"message": "Page Not Found"})

    return render(
        request,
        "encyclopedia/entry.html",
        {"title": util.true_title(title), "content": markdown(entry)},
    )


def search(request):
    q = request.POST["q"].strip()
    entries = util.list_entries()

    if (
        q.lower() in entries
        or q.upper() in entries
        or q.capitalize() in entries
        or q.title() in entries
    ):
        return HttpResponseRedirect(reverse("title", kwargs={"title": q}))

    results = [entry for entry in entries if q.lower() in entry.lower()]

    if len(results) == 0:
        return render(
            request, "encyclopedia/error.html", {"message": f'No results for "{q}"'}
        )

    return render(request, "encyclopedia/search.html", {"q": q, "entries": results})


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")

    post_data = request.POST
    entries = util.list_entries()

    title = post_data["title"]
    content = post_data["content"]

    if (
        title.lower() in entries
        or title.upper() in entries
        or title.capitalize() in entries
        or title.title() in entries
    ):
        return render(
            request, "encyclopedia/error.html", {"message": "Page already exists"}
        )

    util.save_entry(title, content)

    return HttpResponseRedirect(reverse("title", kwargs={"title": title}))


def edit(request, title):
    if request.method == "GET":
        entries = util.list_entries()

        if not (
            title.lower() in entries
            or title.upper() in entries
            or title.capitalize() in entries
            or title.title() in entries
        ):
            return render(
                request, "encyclopedia/error.html", {"message": "Page doesn't exists"}
            )

        return render(
            request,
            "encyclopedia/edit.html",
            {"title": util.true_title(title), "content": util.get_entry(title)},
        )

    content = request.POST["content"]

    util.save_entry(util.true_title(title), content)

    return HttpResponseRedirect(reverse("title", kwargs={"title": title}))


def random(request):
    title = choice(util.list_entries())

    return HttpResponseRedirect(reverse("title", kwargs={"title": title}))
