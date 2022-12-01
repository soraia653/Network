import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Following
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
    
    # fetch all posts
    posts = Post.objects.all()
    posts = posts.order_by("-creation_date").all()

    # apply paginator
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # user liked posts
    try:
        u = User.objects.get(username=request.user)
        liked_posts = u.posts_like.all()
    except:
        liked_posts = []
    
    context_dict = {
        'form': form,
        'page_obj' : page_obj,
        'liked_posts': liked_posts
    }
    return render(request, "network/index.html", context=context_dict)

@csrf_exempt
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'PUT':
        if post.num_likes.filter(id=request.user.id).exists():
            post.num_likes.remove(request.user)
        else:
            post.num_likes.add(request.user)
    
    return HttpResponse(status=204)

@csrf_exempt
def edit_post(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)

        post.text = data.get("text")
        post.save()
            
        return HttpResponse(status=204)
        
    else:
        return JsonResponse({'error': 'PUT request required.'}, status=400)

def following(request):

    # get user object
    u = User.objects.get(username=request.user)

    # fetch who the user follows
    following = u.following.all()

    followed_users = []

    for i in range(following.count()):
        followed_users.append(following[i].following_user)
    
    posts = Post.objects.filter(user__in = followed_users)
    posts = posts.order_by("-creation_date").all()
    
    context_dict = {
        'posts' : posts
    }

    return render(request, "network/following.html", context=context_dict)

def profile_page(request, username):

    # fetch user by username
    u = User.objects.get(username=username)

    # fetch all posts of the user
    user_posts = Post.objects.filter(user=u)
    user_posts = user_posts.order_by('-creation_date').all()

    # count number of user followers
    num_followers = u.followers.all().count()

    # count number of users that the user follows
    num_following = u.following.all().count()

    # check if request.user follows user
    req_user = User.objects.get(username=request.user)
    following = req_user.following.all()

    f_users = []

    for i in range(following.count()):
        if following[0].following_user.username not in f_users:
            f_users.append(following[0].following_user.username)

    # PROCESS FOLLOW REQUEST
    if request.method == 'POST':

        if username not in f_users:
            Following.objects.get_or_create(user=req_user, following_user=u)
            return redirect('profile', username)
        else:
            Following.objects.get(user=req_user, following_user=u).delete()
            return redirect('profile', username)

    context_dict = {
        'n_followers': num_followers,
        'n_following': num_following,
        'username': username,
        'user_posts': user_posts,
        'follows_users': f_users
    }

    return render(request, "network/profile_page.html", context=context_dict)

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
