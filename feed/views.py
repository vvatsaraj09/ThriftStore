from django.shortcuts import render

# Create your views here.
from followers.models import Followers
from products.models import Product


def get_feed(request):
    arr = []
    followers = Followers.objects.filter(follower=request.user)
    for a in followers:
        arr.append(a.following)
    products = get_product_from_followers(arr)
    context = {"obj": products}
    return render(request, "product/feed.html", context)


def get_product_from_followers(followers):
    obj = Product.objects.filter(active=True)
    results = []
    for objs in obj:
        if objs.seller in followers:
            results.append(objs)
            print(results)
    return results
