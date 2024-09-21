from django.shortcuts import render, redirect, get_object_or_404
from django.conf.urls import handler404, handler500, handler403
from django.db.models import Exists, OuterRef, Prefetch, Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.utils.translation import activate
from django.utils import translation
from django.conf import settings
from django.views import View
from django.utils import timezone

from customer_app.models import *
from product_app.models import *
from order_app.models import *
from like_app.models import *
from ads_app.models import *
from customer_app.views import get_customer

from django.utils import timezone
from urllib.parse import urlencode

def custom_set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', settings.LANGUAGE_CODE)
        next_url = request.POST.get('next', '/')
        query_params = request.POST.get('query_params', '')
        settings.LANGUAGE_CODE = language
        activate(language)
        request.session[settings.LANGUAGE_COOKIE_NAME] = language
        request.session['django_language'] = language
        if query_params:
            full_url = f"{next_url}?{query_params}"
        else:
            full_url = next_url
        return HttpResponseRedirect(full_url)
    return HttpResponseRedirect('/')


def home(request):
    categories = ProductCategory.objects.all().prefetch_related('products')
    customer = get_customer(request)
    
    user_order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    user_like, _ = Like.objects.get_or_create(customer=customer)
    
    cart_product_ids = set(user_order.products.values_list('id', flat=True))
    liked_product_ids = set(user_like.products.values_list('id', flat=True))
    
    for category in categories:
        category.name = category.get_translated_category()
        for product in category.products.all():
            product.in_cart = product.id in cart_product_ids
            product.in_like = product.id in liked_product_ids
            product.name = product.get_translated_name()
            product.description = product.get_translated_description()
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
    return render(request, 'index.html', {
        'categories': categories, 
        'ads': ads_list, 
        'brands':brands_list
    })

def search_pill(request):
    customer = get_customer(request)
    current_language = get_language()
    if request.method == "GET":
        search = request.GET.get('searchInput', '').strip()
        results = Product.objects.filter(
            Q(product_name_tm__icontains=search) |
            Q(product_name_ru__icontains=search) |
            Q(product_name__icontains=search)
        ).prefetch_related('images')
        
        
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        user_like, created = Like.objects.get_or_create(customer=customer)

        for product in results:
                product.in_cart = order.products.filter(id=product.id).exists()
                product.in_like = user_like.products.filter(id=product.id).exists()
                product.name = product.get_translated_name()
                product.description = product.get_translated_description()
    return render(request, 'search_pill.html', {'search_products':results})



def custom_404_view(request, exception):
    return render(request, "errors/404.html", status=404)

def custom_403_view(request, exception):
    return render(request, "errors/403.html", status=403)

def custom_500_view(request):
    return render(request, "errors/500.html", status=500)

def restricted_view(request):
    return HttpResponseForbidden()

def server_error_view(request):
    raise Exception("This is a test exception")


# Assigning the custom views to handlers
handler404 = custom_404_view
handler403 = custom_403_view
handler500 = custom_500_view

# Create your views here.
