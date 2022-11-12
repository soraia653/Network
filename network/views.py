import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post
from .forms import PostForm


def index(request):

    # create a new post
    form = PostForm(None)

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            new_post = form.save(commit=False)
            new_post.user = User.objects.get(username=request.user)
            new_post.save()

            return redirect('index')
        else:
            form = PostForm()
    
    context_dict = {
        'form': form
    }
    return render(request, "network/index.html", context=context_dict)


def all_posts(request):

    posts = Post.objects.all()
    posts = posts.order_by("-creation_date").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)

def profile_page(request):
    return render(request, "network/profile_page.html")

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
