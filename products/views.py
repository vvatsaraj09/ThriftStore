from django.shortcuts import render
from .forms import CreateProductForm
from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Product
from django.contrib.auth.models import User
from followers.models import Followers
# from authentication.models import User
from django.contrib import messages
cart = []

def registerProductPage(request):
    form = CreateProductForm(request.POST or None,initial={'seller': request.user,'date' : date.today})
    if form.is_valid():
        form.save()
        form = CreateProductForm()
    context = {'form' : form}
    return render(request,'product/registration.html',context)

def productListPage(request):
    obj = Product.objects.filter(active=True)
    context = {"obj" : obj}
    return render(request, "product/list.html", context)

def productPage(request, id):
    object = Product.objects.get(id=id)
    context = {'object' : object}
    return render(request, "product/product.html", context)

def profilePage(request):
    obj = Product.objects.filter(seller = request.user)
    context = {"obj" : obj}
    return render(request, "product/profile.html", context)

def productCartPage(request, id):
    object = Product.objects.get(id=id)
    if request.method == 'POST':
        cart.append(object)
        print(cart)
    context = {'object' : object}
    return render(request, "product/productCart.html", context)

def cartPage(request):
    context = {"obj" : cart}
    return render(request, "product/cart.html", context)

def feed(request):
    arr = []
    followers = Followers.objects.filter(follower = request.user)
    for a in followers:
        arr.append(a.following)
    obj = Product.objects.filter(active=True)
    results = []
    for objs in obj:
        if objs.seller in arr:
            results.append(objs)
            print(results)
    context = {"obj" : results}
    return render(request, "product/feed.html", context)

def userSearch(request,username):
    object = User.objects.get(username=username)
    objs = Product.objects.filter(seller=object.username )
    fol = Followers.objects.all()
    followers = Followers.objects.filter(follower = request.user)
    flag =  False
    no_followers = 0
    no_following = 0
    for a in fol:
        if a.following == username:
            no_following+=1 
        elif a.followers == username:
            no_followers+=1
    for a in followers:
        if a.following  == username:
            flag =  True 
            break
    context = {'object' : object, "pros":objs, "flag":flag, "followers":no_followers, "following": no_following}
    
    if request.method == 'POST':
        a=Followers()
        a.follower= request.user
        a.following= username
        a.save()
        context = {'object' : object, "pros":objs, "flag":True, "followers":no_followers, "following": no_following}
    return render(request, "product/user_profile.html", context)

def search(request):
    obj = Product.objects.filter(active=True)
    query = request.GET.get('q','')
    query1 = request.GET.get('desc','')
    query2 = request.GET.get('seller','')
    results = []
    if query or query1 or query2:
            for objs in obj:
                try:
                    n = objs.name.index(query)
                    n1 = objs.description.index(query1)
                    n2 = objs.seller.index(query2)
                    results.append(objs)
                except:
                    print("NOT")
            print(len(results))
            if len(results)!=0:
                context = {"obj" : results}
                return render(request, "product/list.html",  context)
            else:
                messages.success(request, 'NO RELEVANT SEARCHES')
                return render(request,"product/search.html")
            
    else:
        results = []
        context = {"obj" : results}
        return render(request,"product/search.html",context)