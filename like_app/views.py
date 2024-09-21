from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from customer_app.views import get_customer
from product_app.models import ProductCategory, Product
from order_app.models import Order

def like_product(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        product = get_object_or_404(Product, id=data)
        customer = get_customer(request)
        like, created = Like.objects.get_or_create(customer=customer)
        product.in_like = like.products.filter(id=product.id).exists()
        if product.in_like:
            likeitem = LikeItem.objects.get(like=like, product_id=product.id)
            likeitem.delete()
        else:
            likeitem, created = LikeItem.objects.get_or_create(like=like, product_id=product.id)
            likeitem.save()
    return render(request, 'index.html')

def favorite(request):
    customer = get_customer(request)
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    user_like, created = Like.objects.get_or_create(customer=customer)
    results = user_like.products.prefetch_related('images')


    # for category in results:
    for product in results:
            product.in_cart = order.products.filter(id=product.id).exists()
            product.in_like = user_like.products.filter(id=product.id).exists()
            product.name = product.get_translated_name()
            product.description = product.get_translated_description()
    return render(request, 'search_pill.html', {'search_products':results})
# Create your views here.
