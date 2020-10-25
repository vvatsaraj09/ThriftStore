from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from followers.models import Followers
from products.models import Product
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from products.views import add_product
from django.contrib import messages


def registerPage(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, "Account was created for " + user)
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'auth/signUp.html', context)


def get_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in as " + username)
            # redirect('')
            return redirect(add_product)
        else:
            messages.info(request, 'Username OR Password is incorrect!')
    context = {}
    return render(request, 'auth/login.html', context)


def update_user(request):
    if request.GET:
        email = request.GET.get('email')
        t = User.objects.get(username=request.user.username)
        t.email = email
        t.save()
        obj = Product.objects.filter(seller=request.user)
        fol = Followers.objects.all()
        no_followers = 0
        no_following = 0
        for a in fol:
            if a.following == request.user.username:
                no_followers += 1
            elif a.follower == request.user.username:
                no_following += 1
            context = {'obj': obj, 'object': request.user, "followers": no_followers, "following": no_following}
        return render(request, "product/profile.html", context)


def homePage(request):
    context = {}
    return render(request, "auth/index.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("auth/login")
