from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

from .models import User, Post
from .forms import NewPostForm

def index(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            print("TEST")
            user = request.user
            content = form.cleaned_data['text']
            new_post = Post(user=user, text=content, date=datetime.now())
            new_post.save()
            
            return render(request, "network/index.html", {
            "form": NewPostForm(),
            "posts": Post.objects.all().order_by('-date'),
            "text_post": content
            })
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by('-date'),
        "form": NewPostForm()
    })


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


def userpage(request, username):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        user_general = User.objects.get(username=username)
        logged_user = User.objects.get(username=request.user.username)
        posts = Post.objects.filter(user=user_general).order_by('-date')
        
        is_following = logged_user.following.filter(username=user_general.username).exists()

        return render(request, "network/userpage.html", {
            "user_general": user_general,
            "logged_user": request.user,
            "posts": posts,
            "is_following": is_following
        })
        
        
def follow_user(request, username):
    if request.method == "POST":
        logged_user = User.objects.get(username=request.user.username)
        user_general = User.objects.get(username=username)
        
        if logged_user.following.filter(username=user_general.username).exists():
            logged_user.following.remove(user_general)
            user_general.followers.remove(logged_user)
        else:
            logged_user.following.add(user_general)
            user_general.followers.add(logged_user)
    
        return redirect('userpage', username=user_general.username)
        # return render(request, "network/userpage.html", {
        #     "user_general": user_general,
        #     "logged_user": logged_user,
        #     "posts": Post.objects.filter(user=user_general).order_by('-date'),
        #     "is_following": is_following
        # })
    else:
        return HttpResponseRedirect(reverse("index"))