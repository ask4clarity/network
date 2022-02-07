from tkinter import E
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django import forms 
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Post, Follow

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['Owner', 'Likes']


def index(request):
    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        if request.user.is_authenticated:
            #Submit the user post 
            p = PostForm(request.POST)
            if p.is_valid(): 
                new_post = p.save(commit=False)
                new_post.Owner = User.objects.get(username=request.user.username)
                new_post.save()
                p.save()
            else:
                messages.error(request, 'Error saving form')
        else:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "network/index.html", {
    "form": PostForm(), 
    "page_obj": page_obj
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

@login_required(login_url='/login')
def user(request, profile):
    owner = get_object_or_404(User, username=profile)
    follower = User.objects.get(username=request.user.username)
    follows = Follow.objects.filter(Owner=follower, Target=owner).first()
    posts = owner.poster.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    follow_count = Follow.objects.filter(Target=owner).count
    following_count = Follow.objects.filter(Owner=owner).count
    #follow or unfollow
    if request.method == "POST":
        if 'add' in request.POST:
            follow = Follow.objects.create(Owner=follower, Target=owner)
            follow.save 
        else:
            follows.delete()
        return redirect(f"/{profile}")
    return render(request, "network/user.html", {
        "page_obj": page_obj,
        "profile": profile,
        "following": follows,
        "follow_count": follow_count,
        "following_count": following_count,
        "owner": owner,
        "user": follower
    })

@login_required(login_url='/login')
def following(request):
    current_user = get_object_or_404(User, username=request.user.username)
    following = Follow.objects.filter(Owner=current_user)
    posts = Post.objects.all().order_by('id').reverse()
    following_posts = []
    for p in posts:
        for f in following:
            if f.Target == p.Owner:
                following_posts.append(p)
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
            "page_obj": page_obj
    })

@csrf_exempt
def edit(request, id):
    post = Post.objects.get(id=id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.Content = data["content"]
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
def like(request, id):
    post = Post.objects.get(id=id)
    user = User.objects.get(username=request.user.username)

    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data.get("like"))
        if data.get("like"):
            post.Likes.add(user)
        else:
            post.Likes.remove(user)
        post.save()
        return HttpResponse(status=204)