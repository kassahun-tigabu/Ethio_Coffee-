from django.shortcuts import render

def home(request):
    return render(request, "frontend/index.html")

def products(request):
    return render(request, "frontend/products.html")

def about(request):
    return render(request, "frontend/about.html")

def contact(request):
    return render(request, "frontend/contact.html")

def cart(request):
    return render(request, "frontend/cart.html")
