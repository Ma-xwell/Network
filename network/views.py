from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post
from .forms import NewPostForm

# def listing(request):
#     contact_list = Contact.objects.all()
#     paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'list.html', {'page_obj': page_obj})

def index(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            user = request.user
            content = form.cleaned_data['text']
            new_post = Post(user=user, text=content, date=datetime.now())
            new_post.save()
            
            posts = Post.objects.all().order_by('-date')
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'network/index.html', {
                "form": NewPostForm(),
                "page_obj": page_obj,
                "text_post": content,
                "posts": posts
            })
            
            # return render(request, "network/index.html", {
            # "form": NewPostForm(),
            # "posts": Post.objects.all().order_by('-date'),
            # "text_post": content
            # })
            
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        "form": NewPostForm(),
        "page_obj": page_obj,
        "posts": posts
    })       
    # return render(request, "network/index.html", {
    #     "posts": Post.objects.all().order_by('-date'),
    #     "form": NewPostForm()
    # })
    
    
@login_required    
def following_posts(request):
    logged_user = User.objects.get(username=request.user.username)
    following = logged_user.following.all()
    followers_posts = Post.objects.filter(user__in=following).order_by('-date')
    paginator = Paginator(followers_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following-posts.html", {
        "page_obj": page_obj,
        "posts": followers_posts,
        "following_number": following.count()
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
        posts = Post.objects.filter(user=user_general).order_by('-date')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.user.username:
            logged_user = User.objects.get(username=request.user.username)
            is_following = logged_user.following.filter(username=user_general.username).exists()
            return render(request, "network/userpage.html", {
                "page_obj": page_obj,
                "user_general": user_general,
                "logged_user": request.user,
                "posts": posts,
                "is_following": is_following
            })
        return render(request, "network/userpage.html", {
            "page_obj": page_obj,
            "user_general": user_general,
            "posts": posts
        })
        
@csrf_exempt      
def get_number_of_followers(request, username):
    if request.method == "POST":
        user_general = User.objects.get(username=username)
        number_of_followers = user_general.followers.count()
        return JsonResponse({"followers": number_of_followers}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
        
@csrf_exempt        
def follow_user(request, username):
    if request.method == "POST":
        logged_user = User.objects.get(username=request.user.username)
        user_general = User.objects.get(username=username)
        
        is_following = logged_user.following.filter(username=user_general.username).exists()
        
        if is_following:
            logged_user.following.remove(user_general)
            user_general.followers.remove(logged_user)
            
        else:
            logged_user.following.add(user_general)
            user_general.followers.add(logged_user)

        is_following = not is_following

        return JsonResponse({"action": f"{'follow' if is_following else 'unfollow'}"}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
    
    
@csrf_exempt
@login_required
def update_post(request, id):
    if request.method == "POST":
        logged_user = User.objects.get(username=request.user.username)
        logged_user_posts = logged_user.post_set.all()
        post = Post.objects.filter(id=id)
        if post[0] in logged_user_posts:
            new_text = request.body.decode('utf-8')
            post.update(text=new_text)
            return JsonResponse({"result": "Update successful"}, status=201)
        return JsonResponse({"result": "Trying to edit other user's post"}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
    

@csrf_exempt
@login_required
def get_new_post(request, id):
    if request.method == "POST":
        logged_user = User.objects.get(username=request.user.username)
        logged_user_posts = logged_user.post_set.all()
        post = Post.objects.filter(id=id)
        if post[0] in logged_user_posts:
            return JsonResponse({"updatedText": post[0].text}, status=201)
        return JsonResponse({"updatedText": "Trying to edit other user's post"}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
@login_required
def like_post(request, id):
    if request.method == "POST":
        logged_user = User.objects.get(username=request.user.username)
        post = Post.objects.get(id=id)
        logged_user_liked_posts = logged_user.liked_posts.all()
        if post in logged_user_liked_posts:
            logged_user.liked_posts.remove(post)
            post.likes -= 1
        else:
            logged_user.liked_posts.add(post)
            post.likes += 1
        post.save()
        return JsonResponse({"like": "success"}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
@login_required
def get_number_of_likes(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        return JsonResponse({"likes": post.likes}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
    
# def listing(request):
#     contact_list = Contact.objects.all()
#     paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'list.html', {'page_obj': page_obj})