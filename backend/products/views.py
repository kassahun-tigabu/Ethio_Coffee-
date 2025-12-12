from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category, CoffeeProduct
from .serializers import CategorySerializer, CoffeeProductSerializer

def product_list(request):
    category_slug = request.GET.get('category')
    region = request.GET.get('region')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')
    
    products = CoffeeProduct.objects.filter(is_available=True)
    
    # Filtering
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    if region:
        products = products.filter(region=region)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    
    categories = Category.objects.all()
    
    context = {
        'products': products_page,
        'categories': categories,
        'selected_category': category_slug,
        'selected_region': region,
        'sort': sort,
    }
    
    return render(request, 'products/list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(CoffeeProduct, slug=slug)
    related_products = CoffeeProduct.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'products/detail.html', context)

# API Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CoffeeProductViewSet(viewsets.ModelViewSet):
    queryset = CoffeeProduct.objects.filter(is_available=True)
    serializer_class = CoffeeProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'region']
    ordering_fields = ['price', 'created_at', 'name']