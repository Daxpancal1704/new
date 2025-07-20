"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .import views

urlpatterns = [
       path('', views.index, name='index'),
       path('shop', views.shop, name='shop'),
       path('detail/<int:id>', views.detail, name='detail'),
       path('contact', views.contact, name='contact'),
       path('checkout', views.checkout, name='checkout'),
       path('cart', views.cart, name='cart'),
       path('plus/<int:id>', views.plus, name='plus'),
       path('minus/<int:id>', views.minus, name='minus'),
       path('deletes/<int:id>', views.deletes, name='deletes'),
       path('address', views.address, name='address'),
       path('delete_Address', views.delete_Address, name='delete_Address'),
       path('login', views.login, name='login'),
       path('register', views.register, name='register'),
       path('confirm_password', views.confirm_password, name='confirm_password'),
       path('forget_password', views.forget_password, name='forget_password'),
       path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
       path('wishlist', views.wishlist, name='wishlist'),
       path('add_to_wishlist/<int:id>', views.add_to_wishlist, name='add_to_wishlist'),
       path('delete_w/<int:id>', views.delete_w, name='delete_w'),
       path('logout', views.logout, name='logout'),
       path('search', views.search, name='search'),
       path('category/<int:id>', views.category, name='category'),
       path('order', views.order, name='order'),
       path('price_filter1', views.price_filter1, name='price_filter1'),




       
]

