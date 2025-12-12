from django.contrib import admin
from django.urls import path
#from main import views
from coffeeapp import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
]

