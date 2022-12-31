from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('collection',views.collections,name='collection'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('cart',views.cart_page,name='cart'),
    path('removetocart/<str:cid>',views.remove_to_cart,name='removetocart'),
    path('favourite',views.favourite_page,name='favourite'),
    path('fav',views.fav_page,name='fav'),
    path('removetofav/<str:cid>',views.remove_to_fav,name='removetofav'),
    path('contacts',views.contact,name="contacts"),
    path('about',views.about.as_view(),name="about"),

    path('collection/<str:name>',views.collectionsview,name='collection'),
    path('collection/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),

]

