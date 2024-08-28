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

from django.utils import timezone
from django.shortcuts import render

def home(request):
    categories = ProductCategory.objects.all().prefetch_related('products')
    customer = get_customer(request)
    # Fetch user order and likes
    user_order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    user_like, _ = Like.objects.get_or_create(customer=customer)
    # Pre-fetch product IDs in cart and likes
    cart_product_ids = set(user_order.products.values_list('id', flat=True))
    liked_product_ids = set(user_like.products.values_list('id', flat=True))
    # Annotate products with in_cart and in_like
    for category in categories:
        for product in category.products.all():
            product.in_cart = product.id in cart_product_ids
            product.in_like = product.id in liked_product_ids
    ads = Advertisement.objects.filter(end_date__gt=timezone.now(), is_brand=False).prefetch_related('images')
    ads_list = []
    active_ad_ids = set()
    for ad in ads:
        ads_images = [{'image': image.image.url} for image in ad.images.all()]
        ads_list.append({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'image': ads_images,
            'url': ad.url
        })
        active_ad_ids.add(ad.id)
    brands = Advertisement.objects.filter(end_date__gt=timezone.now(), is_brand=True).prefetch_related('images')
    brands_list = []
    for ad in brands:
        brands_images = [{'image': image.image.url} for image in ad.images.all()]
        brands_list.append({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'image': brands_images,
            'url': ad.url
        })
        active_ad_ids.add(ad.id)
    
    Advertisement.objects.filter(id__in=active_ad_ids).update(is_active=True)
    Advertisement.objects.exclude(id__in=active_ad_ids).update(is_active=False)
    return render(request, 'index.html', {'categories': categories, 'ads': ads_list, 'brands':brands_list})

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
