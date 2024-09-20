from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_language
from customer_app.views import get_customer
from order_app.models import *
from like_app.models import *
from .models import *

def custom_pills(request, category_id):
    spec_category = ProductCategory.objects.all().filter(id=category_id).prefetch_related('products')
    customer = get_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    user_like, created = Like.objects.get_or_create(customer=customer)
    for category in spec_category:
        category.name = category.get_translated_category()
        for product in category.products.all():
            product.in_cart = order.products.filter(id=product.id).exists()
            product.in_like = user_like.products.filter(id=product.id).exists()
            product.description = product.get_translated_description()
            product.name = product.get_translated_name()
    return render(request, 'custom_category.html', {'spec_categories':spec_category})

def product(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        customer =  get_customer(request)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        product.in_cart = order.products.filter(id=data).exists()
        if product.in_cart:
            orderItem = OrderItem.objects.get(order=order, product_id=data)
            orderItem.delete()
            status = 'deleted'
        else:
            orderItem, created = OrderItem.objects.get_or_create(order=order, product_id=data)
            orderItem.save()
            status = 'saved'
    categories = ProductCategory.objects.all().prefetch_related('products')
    return JsonResponse({'total_quantity':order.get_total_quantity(), 'status':status, 'lang':get_language()})

def profile(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = product.category_name.all()
    images = product.images.all()
    customer = get_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    user_like, created = Like.objects.get_or_create(customer=customer)

    translated_categories = [category.get_translated_category() for category in categories]

    product.in_cart = order.products.filter(id=product_id).exists()
    product.in_like = user_like.products.filter(id=product_id).exists()
    product.description = product.get_translated_description()
    product.name = product.get_translated_name()
    return render(request, 'product_profile.html', {"product_cat":translated_categories, 'images':images, "product":product})
# Create your views here.
