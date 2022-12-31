from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from shop.form import CustomUserForm
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views import generic

# Create your views here.

class about(generic.ListView):
    model= Catagory
    template_name="shop/about.html"

def home(request):
    Products=product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"Products":Products})

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        body=request.POST.get('body')
        print(name,email,body)
        send_mail(
            'caddcenter - chat',
             name + "-" +body,
             email,
            ['ratha98arul@gmail.com'],
            fail_silently=False,
        )
        
    return render(request,"shop/contacts.html")


def remove_to_fav(request,cid):
    cartitem=Favourite.objects.get(id=cid)
    cartitem.delete()
    return redirect('/fav')

def fav_page(request):
    if request.user.is_authenticated:
        favourite=Favourite.objects.filter(User=request.user)
        return render(request,"shop/fav.html",{"favourite":favourite})
    else:
        return redirect('/')
    

def favourite_page(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            #print(request.user.id)
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(User=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in favourite'},status=200)
                else:
                    Favourite.objects.create(User=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to favourite'},status=200)
                    
        else:
            return JsonResponse({'status':'Login to add favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    



def remove_to_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')


def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(User=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect('/')

def add_to_cart(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(User=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(User=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to add cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)



def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logged out successfully")
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            User=authenticate(request,username=name,password=pwd)
            if User is not None:
                login(request,User)
                messages.success(request,"login successfully")
                return redirect('/')
            else:
                messages.error(request,"invalid username or password")
                return redirect('/login')
    return render(request,"shop/login.html")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registeration success you can log now ")
            return redirect('/login')
    return render(request,"shop/register.html",{"form":form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/collection.html",{"Catagory":catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        Products=product.objects.filter(Catagory__name=name)
        return render(request,"shop/products/index.html",{"Products":Products,"catagory_name":name})
    else:
        messages.warning(request, "NO such catagory found")
        return redirect("collection")

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            Products=product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"Products":Products})
        else:
            messages.warning(request, "NO such catagory found")
            return redirect("collection")
    else:
        messages.warning(request, "NO such catagory found")
        return redirect("collection")
    




