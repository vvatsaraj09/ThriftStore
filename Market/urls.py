"""Market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from authentication.views import *
from products.views import *
from followers.views import *
from feed.views import *

from django.views.generic import RedirectView

urlpatterns = [
    path('products/profile', profilePage, name="Profile"),
    # path('products/list/<int:id>/', productPage, name="Product"),
    # path('products/list/', productListPage, name="ProductList"),
    path('products/search/', search_product, name="searchList"),
    path('products/search/add_follower/', add_follower, name="add_follower"),
    path('products/search/delete_follower/', delete_follower, name="delete_follower"),
    path('products/search/view_connections/', view_connections, name="view_connections"),
    path('products/search/profile/', update_product, name="update_product"),
    path('products/search/profile/update_user', update_user, name="update_user"),

    path('', RedirectView.as_view(url='/auth/index')),
    path('products/register/', add_product, name="Register"),
    path('auth/login/', get_user, name="Login"),
    path('auth/index/', homePage, name="Home"),
    path('auth/login/', logout, name="Logout"),
    path('products/feed/', get_feed, name="Feed"),
    path('auth/register/', add_user, name="Sign Up"),
    path('admin/', admin.site.urls),
]
