from django.shortcuts import render

def index(request):
    return render(request, 'buyers/index.html', locals())

def login(request):
    return render(request, 'buyers/login.html', locals())

def cart(request):
    return render(request, 'buyers/cart.html', locals())

def products(request):
    return render(request, 'buyers/products.html', locals())

def product_details(request):
    return render(request, 'buyers/product_details.html', locals())