from .forms import CreateProductForm
from datetime import date

from django.contrib import messages
import geocoder

from followers.views import *

# from django.contrib.gis.geoip import GeoIP
cart = []


# g = GeoIP()

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

def add_product(request):
    # print(request)
    # g = geocoder.ip('me')
    # print(g.latlng)

    g = geocoder.ip('me')
    lattitude = g.latlng[0]
    longitude = g.latlng[1]
    form = CreateProductForm(request.POST or None,
                             initial={'seller': request.user, 'date': date.today, 'lattitude': lattitude,
                                      'longitude': longitude})
    if form.is_valid():
        form.save()
        form = CreateProductForm()
    context = {'form': form}
    return render(request, 'product/registration.html', context)


def productListPage(request):
    obj = Product.objects.filter(active=True)
    context = {"obj": obj}
    return render(request, "product/list.html", context)


def productPage(request, id):
    object = Product.objects.get(id=id)
    context = {'object': object}
    return render(request, "product/product.html", context)


def profilePage(request):
    # print(g.lon_lat())
    obj = Product.objects.filter(seller=request.user)
    fol = Followers.objects.all()
    no_followers = 0
    no_following = 0
    print(fol)
    for a in fol:
        if a.following == request.user.username:
            no_followers += 1
        elif a.follower == request.user.username:
            no_following += 1
        context = {'obj': obj, 'object': request.user, "followers": no_followers, "following": no_following}
    return render(request, "product/profile.html", context)


def productCartPage(request, id):
    object = Product.objects.get(id=id)
    if request.method == 'POST':
        cart.append(object)
        print(cart)
    context = {'object': object}
    return render(request, "product/productCart.html", context)


def update(request):
    if request.GET:
        name = request.GET.get('name')
        description = request.GET.get('description')
        print(name, description)
        t = Product.objects.get(name=name, description=description)
        t.active = False
        t.save()
        obj = Product.objects.filter(seller=request.user)
        fol = Followers.objects.all()
        no_followers = 0
        no_following = 0
        print(fol)
        for a in fol:
            if a.following == request.user.username:
                no_followers += 1
            elif a.follower == request.user.username:
                no_following += 1
            context = {'obj': obj, 'object': request.user, "followers": no_followers, "following": no_following}
        return render(request, "product/profile.html", context)


def geter(a):
    g = geocoder.ip('me')
    lattitude = g.latlng[0]
    longitude = g.latlng[1]
    return abs(int(lattitude) - int(a.lattitude)) + abs(int(longitude) - int(a.longitude))


def search_product(request):
    if request.method == "GET":
        obj = Product.objects.filter(active=True)
        query = request.GET.get('q', '')
        query1 = request.GET.get('desc', '')
        query2 = request.GET.get('seller', '')
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
            results.sort(key=geter)
            if len(results) != 0:
                context = {"obj": results}
                return render(request, "product/list.html", context)
            else:
                messages.success(request, 'NO RELEVANT SEARCHES')
                return render(request, "product/search.html")

        else:
            results = []
            context = {"obj": results}
            return render(request, "product/search.html", context)
    if request.method == "POST":
        username = request.POST.get('user', '')
        object = User.objects.get(username=username)
        objs = Product.objects.filter(seller=object.username)
        fol = Followers.objects.all()
        followers = Followers.objects.filter(follower=request.user)
        flag = False
        no_followers = 0
        no_following = 0
        for a in fol:
            if a.following == username:
                no_following += 1
            elif a.follower == username:
                no_followers += 1
        for a in followers:
            if a.following == username:
                flag = True
                break
        context = {'object': object, "pros": objs, "flag": flag, "followers": no_followers, "following": no_following}
        return render(request, "product/user_profile.html", context)
