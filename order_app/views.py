from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from .models import *
from customer_app.views import get_customer

def cart(request):
    customer =  get_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitems.select_related('product').prefetch_related('product__images')
    shipping_price = ShippingConfig.get_solo().shipping_price
    shipping_regions = ShippingRegion.objects.all()
    context = {
        'items':items,
        'order_id':order.id,
        'total_price':order.get_total_price(),
        'total_items_price':order.get_total_items_price(),
        'shipping_price':shipping_price,
        'shipping_regions':shipping_regions,
        'total_quantity':order.get_total_quantity()
    }
    return render(request, 'basket.html', context)

def quantity_increase(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        customer =  get_customer(request)    
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        product = OrderItem.objects.get(order=order, product_id=data)
        if product.quantity < product.product.stock:
            quantity = product.quantity + 1
            product.quantity = quantity
            product.save()
        return JsonResponse({
            'quantity':product.quantity,
            'total_price':order.get_total_price(),
            'total_items_price':order.get_total_items_price(),
            'total_quantity':order.get_total_quantity()})
    return render(request, 'basket.html')

def quantity_decrease(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        customer =  get_customer(request)    
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        product = OrderItem.objects.get(order=order, product_id=data)
        quantity = product.quantity - 1
        product.quantity = quantity
        product.save()
        return JsonResponse({
            'quantity':product.quantity, 
            'total_price':order.get_total_price(), 
            'total_items_price':order.get_total_items_price(),
            'total_quantity':order.get_total_quantity()})
    return render(request, 'basket.html')

def item_remove(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        customer =  get_customer(request)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        product = OrderItem.objects.get(order=order, product_id=data)
        product.delete()
        return JsonResponse({
            'total_price':order.get_total_price(), 
            'total_items_price':order.get_total_items_price(),
            'total_quantity':order.get_total_quantity()})
    return render(request, 'basket.html')

def order_remove(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        customer =  get_customer(request)
        order, created = Order.objects.get_or_create(id=data,customer=customer, complete=False)
        orderitem = OrderItem.objects.all().filter(order=order)
        orderitem.delete()
        return JsonResponse({
            "data":'deleted', 
            'total_price':order.get_total_price(), 
            'total_items_price':order.get_total_items_price(),
            'total_quantity':order.get_total_quantity()})
    return render(request, 'basket.html')

def shipping(request):
    customer = get_customer(request)
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        phone_number = request.POST.get('phoneNumber')
        region_id  = request.POST.get('regionName')
        shipping_street = request.POST.get('shippingStreet')
        shipping_note = request.POST.get('shippingNote')
        pay_type = request.POST.get('payType')

        region_name = get_object_or_404(ShippingRegion, id=region_id)

        order = Order.objects.get(customer=customer, complete=False)
        shipping_address = ShippingAddress.objects.create(customer=customer, customer_name=full_name, phone_number=phone_number, order=order, region_name=region_name, address=shipping_street, note=shipping_note, payment_type=pay_type)
        order.complete = True
        order.save()
        order = Order.objects.create(customer=customer, complete=False)
    return JsonResponse({'total_quantity':order.get_total_quantity()})
# Create your views here.
