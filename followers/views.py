from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from followers.models import Followers
from products.models import Product


def add_follower(request):
    if request.GET:
        username = request.GET.get('username')
        a = Followers()
        a.follower = request.user
        a.following = username
        a.save()
        object = User.objects.get(username=username)
        objs = Product.objects.filter(seller=object.username)
        fol = Followers.objects.all()
        followers = Followers.objects.filter(follower=request.user)
        flag = False
        no_followers = 0
        no_following = 0
        for a in fol:
            if a.following == username:
                no_followers += 1
            elif a.follower == username:
                no_following += 1
        for a in followers:
            if a.following == username:
                flag = True
                break
        context = {'object': object, "pros": objs, "flag": flag, "followers": no_followers, "following": no_following}
        return render(request, "product/user_profile.html", context)


def delete_follower(request):
    if request.GET:
        username = request.GET.get('username')
        a = Followers.objects.get(follower=request.user.username, following=username)
        a.delete()
        object = User.objects.get(username=username)
        objs = Product.objects.filter(seller=object.username)
        fol = Followers.objects.all()
        followers = Followers.objects.filter(follower=request.user)
        flag = False
        no_followers = 0
        no_following = 0
        for a in fol:
            if a.following == username:
                no_followers += 1
            elif a.follower == username:
                no_following += 1
        for a in followers:
            if a.following == username:
                flag = True
                break
        context = {'object': object, "pros": objs, "flag": flag, "followers": no_followers, "following": no_following}
        return render(request, "product/user_profile.html", context)


def get_followers(request, username):
    arr = []
    followers = Followers.objects.filter(following=username)
    for a in followers:
        arr.append(a.follower)
    return arr


def get_following(request, username):
    arr = []
    following = Followers.objects.filter(follower=username)
    for a in following:
        arr.append(a.following)
    return arr


def view_connections(request):
    followers = get_followers(request, request.user.username)
    following = get_following(request, request.user.username)
    context = {'followers': followers, 'following': following, 'object': request.user, 'l1': len(followers),
               'l2': len(following)}
    print(followers, following)
    return render(request, "product/view_connections.html", context)
