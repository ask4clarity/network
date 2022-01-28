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

from .models import User, Post, Follow

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['Owner', 'Likes']


def index(request):
    posts = Post.objects.all().order_by('id').reverse()
    if request.method == "POST":
        #Submit the user post 
        p = PostForm(request.POST)
        if p.is_valid(): 
            new_post = p.save(commit=False)
            new_post.Owner = User.objects.get(username=request.user.username)
            new_post.save()
            p.save()
        else:
            messages.error(request, 'Error saving form')
    return render(request, "network/index.html", {
    "posts": posts,
    "form": PostForm() 
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

def user(request, profile):
    owner = get_object_or_404(User, username=profile)
    follower = User.objects.get(username=request.user.username)
    follows = Follow.objects.filter(Owner=follower, Target=owner).first()
    posts = owner.poster.all().order_by('id').reverse()
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
        "posts": posts,
        "profile": profile,
        "following": follows,
        "follow_count": follow_count,
        "following_count": following_count,
        "owner": owner,
        "user": follower
    })

def following(request):
    current_user = get_object_or_404(User, username=request.user.username)
    following = Follow.objects.filter(Owner=current_user)
    following_posts = []
    for f in following:
        prof_posts = Post.objects.filter(Owner=f.Target)
        following_posts.extend(prof_posts)
    return render(request, "network/following.html", {
        "posts": following_posts
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