from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Exists, OuterRef, Prefetch
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils import timezone

from customer_app.models import *
from product_app.models import *
from order_app.models import *
from like_app.models import *
from ads_app.models import *
from customer_app.views import get_customer

def home(request):
    categories = ProductCategory.objects.all().prefetch_related('products')
    customer = get_customer(request)
    user_order, created = Order.objects.get_or_create(customer=customer, complete=False)
    user_like, created = Like.objects.get_or_create(customer=customer)
    for category in categories:
        for product in category.products.all():
            product.in_cart = user_order.products.filter(id=product.id).exists()
            product.in_like = user_like.products.filter(id=product.id).exists()
    ads = Advertisement.objects.filter(end_date__gt=timezone.now()).prefetch_related('images')
    ads_list = []
    for ad in ads:
        ads_images = []
        for image in ad.images.all():
            ads_images.append({
                    'image': image.image.url
            })
        ads_list.append({
            'id': ad.id,
            'title':ad.title,
            'description': ad.description,
            'image': ads_images,
            'url':ad.url
        })
    all_ads = Advertisement.objects.all().filter()
    for ad in all_ads:
        if ad not in ads_list:
            ad.is_active = False
        else:
            ad.is_active=True
        ad.save()
    return render(request, 'index.html', {'categories': categories, 'ads':ads_list})

def search_pill(request):
    customer = get_customer(request)
    if request.method == "GET":
        search = request.GET.get('searchInput', '').strip()
        print(search)
        results = Product.objects.filter(product_name__icontains=search).prefetch_related('images')
        
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        user_like, created = Like.objects.get_or_create(customer=customer)

        # for category in results:
        for product in results:
                product.in_cart = order.products.filter(id=product.id).exists()
                product.in_like = user_like.products.filter(id=product.id).exists()
    return render(request, 'search_pill.html', {'search_products':results})

def base(request):
    pass
# Create your views here.
