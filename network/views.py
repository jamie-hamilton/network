from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import json
from datetime import datetime

from .models import User, Post, Connect, Like
from . import forms


def index(request):
    """View all user posts and allow for new post when logged in"""
    posts = Post.objects.all().order_by('-date')

    # Post pagination: https://docs.djangoproject.com/en/3.1/topics/pagination/
    index_paginator = Paginator(posts, 10)
    index_page = request.GET.get('page')
    page_obj = index_paginator.get_page(index_page)

    if request.method == "POST":
        # Get post form data for new post
        form = forms.PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.info(request, 'Shout delivered!')
            return redirect("index")
        else:
            messages.error(request, 'Shout failed - please try again.')
            return redirect("index")

    else:
        # PostForm forms.py
        form = forms.PostForm()

    context = {'page_obj': page_obj, 'post_form': form}
    return render(request, "network/index.html", context)


@login_required(login_url="login")
def profile(request, username):
    """View user profile"""
    if request.method == "GET":
        # Retrieve profile user by request URL
        profile_user = User.objects.get(username=username)

        # Post pagination: https://docs.djangoproject.com/en/3.1/topics/pagination/
        posts = profile_user.posts.all().order_by("-date")
        profile_paginator = Paginator(posts, 10)
        profile_page = request.GET.get('page')
        page_obj = profile_paginator.get_page(profile_page)
    else:
        return redirect("index")

    context = {'profile_user': profile_user, 'page_obj': page_obj, 'photo_form': forms.UploadPhotoForm()}
    return render(request, "network/profile.html", context)


@login_required(login_url="login")
def following(request):
    """View all posts from followed users"""
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        following = user.follow_list.following.all()

        # Post pagination: https://docs.djangoproject.com/en/3.1/topics/pagination/
        posts = Post.objects.filter(user__in=following).order_by("-date")
        following_paginator = Paginator(posts, 10)
        following_page = request.GET.get('page')
        page_obj = following_paginator.get_page(following_page)
    else:
        return redirect("index")
    context = {"page_obj": page_obj}
    return render(request, "network/following.html", context)


@login_required(login_url="login")
def edit(request, user_id, post_id):
    """Handle edit post requests"""
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            post = Post.objects.get(pk=post_id)
            # Ensure request is coming from correct user
            if post.user.id != request.user.id:
                return JsonResponse({
                        "error": "User isn't authorised to make this request."
                    }, status=403)
            else:
                # Update post and add 'edited' timestamp
                post.post = data.get('edited')
                post.edited = datetime.now()
                post.save()
        except Post.DoesNotExist:
            return JsonResponse({"error": "Edit request not recognised."}, status=404)
    else:
        # Bad request error if wrong request received
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

    # Response if successful
    return JsonResponse(
        {
            "message": "Post updated!", 
            "post": post.post, 
            "date_edited": post.edited.strftime(" - Edited at %H:%M on %d/%m/%y")
        }, status=204)


@login_required(login_url="login")
def like(request, post_id):
    """Handle like/unlike requests"""
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = int(data['user'])
        
        # Ensure request is coming from correct user
        if user_id != request.user.id:
            return JsonResponse({
                    "error": "User isn't authorised to make this request."
                }, status=400)
        else:
            user = User.objects.get(pk=user_id)
            # check that post still exists
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "This post has been removed."}, status=404)

            # if like exists user must've unliked
            try:
                # try unlike
                like = Like.objects.get(post=post, user=user.id)
                like.delete()

                # Successully deleted:
                return JsonResponse({"message": "Post cooled"}, status=204)

            except Like.DoesNotExist:
                # create like
                like = Like.objects.create(post=post, user=user)

                # Successfully created:
                return JsonResponse({"message": "Ouch, that post is hot"}, status=201)
    else:
        # Bad request error if wrong request received
        return JsonResponse({
            "error": "POST request required."
        }, status=400)


@login_required(login_url="login")
def connect(request, profile_user):
    """Retrieve follower data and handle follow/unfollow requests"""
    # Check user exists
    try:
        profile_user = User.objects.get(pk=profile_user)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Get following/followers and return as JSON objects
    if request.method == "GET":
        connections, created = Connect.objects.get_or_create(current_user=profile_user)
        context = {"followers": list(User.objects.filter(follow_list__following=profile_user).values('id', 'username')),
                   "following": list(connections.following.all().values('id', 'username')), 
                   "user": list(User.objects.filter(pk=request.user.id).values('id', 'username'))}

        return JsonResponse(context, safe=False)

    # Handle follow/unfollow requests
    elif request.method == "PUT":
        data = json.loads(request.body)

        # use class methods from Connect model to follow or unfollow
        if data.get("call") == "Follow":
            Connect.follow(request.user, profile_user)
        elif data.get("call") == "Unfollow":
            Connect.unfollow(request.user, profile_user)
        else:
            # Unsuccessful response
            return JsonResponse({
                "error": "Follow/unfollow request not recognised."
            }, status=400)

        # Successful response
        return JsonResponse({"message": "Follow/unfollow request successful!"}, status=204)

    else:
        # Bad request error if wrong request received
        return JsonResponse({
            "error": "PUT or GET request required."
        }, status=400)



@login_required(login_url="login")
def upload(request, username):
    """Handle user photo uploads"""
    if request.method == 'POST':
        # check validity of request
        form = forms.UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid() and request.user.username == username:
            new_pic = form.cleaned_data["profile_image"]
            user = User.objects.get(username=username)

            # delete previous profile image
            if user.profile_image:
                user.profile_image.delete()
            
            # add new profile image
            user.profile_image = new_pic
            user.save()
            messages.info(request, 'Upload successful.')
            return redirect('profile', username=username)

        else:
            messages.error(request, "Sorry, something went wrong - please try again.")
            return redirect('profile', username=username)

    return redirect('index')


def login_view(request):
    """Log users in"""
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    """Log users out"""
    logout(request)
    return redirect("index")


def register(request):
    """Register new users"""
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
        return redirect("index")
    else:
        return render(request, "network/register.html")
