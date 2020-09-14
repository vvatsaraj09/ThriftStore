from django.shortcuts import render
from .forms import CreateProductForm
from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Product
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
    obj = Product.objects.filter(active=True)
    context = {'object':obj}
    return render(request,"product/search.html",context)
    
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