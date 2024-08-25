from django.shortcuts import render
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
        for product in category.products.all():
            product.in_cart = order.products.filter(id=product.id).exists()
            product.in_like = user_like.products.filter(id=product.id).exists()
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
        else:
            orderItem, created = OrderItem.objects.get_or_create(order=order, product_id=data)
            orderItem.save()
    categories = ProductCategory.objects.all().prefetch_related('products')
    return render(request, 'index.html', {'categories':categories})
# Create your views here.
