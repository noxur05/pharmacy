from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import json
from .models import *
from .serializers import OrderItemSerializer
from customer_app.views import get_customer
from product_app.models import ProductCategory, Product

def cart(request):
    customer =  get_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitems.select_related('product').prefetch_related('product__images')
    for item in items:
        item.product.name = item.product.get_translated_name()
        item.product.description = item.product.get_translated_description()
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

@api_view(['POST'])
def quantity_increase(request):
    data = request.data.get('data')
    customer =  get_customer(request)    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    product = OrderItem.objects.get(order=order, product_id=data)
    if product.quantity < product.product.stock:
        quantity = product.quantity + 1
        product.quantity = quantity
        product.save()
    return Response({
        'quantity':product.quantity,
        'total_price':order.get_total_price(),
        'total_items_price':order.get_total_items_price(),
        'total_quantity':order.get_total_quantity()}, status=status.HTTP_200_OK)
    return render(request, 'basket.html')

@api_view(['POST'])
def quantity_decrease(request):
    data = request.data.get('data')
    customer =  get_customer(request)    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    product = OrderItem.objects.get(order=order, product_id=data)
    quantity = product.quantity - 1
    product.quantity = quantity
    product.save()
    return Response({
        'quantity':product.quantity, 
        'total_price':order.get_total_price(), 
        'total_items_price':order.get_total_items_price(),
        'total_quantity':order.get_total_quantity()}, status=status.HTTP_200_OK)
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

@api_view(['POST'])
def order_remove(request):
    data = request.data.get("data")
    if data != None:
        print(data)
        customer =  get_customer(request)
        order, created = Order.objects.get_or_create(id=data, customer=customer, complete=False)
        orderitem = OrderItem.objects.filter(order=order)
        orderitem.delete()
        return Response({
            "data":'deleted', 
            'total_price':order.get_total_price(), 
            'total_items_price':order.get_total_items_price(),
            'total_quantity':order.get_total_quantity()}, status=status.HTTP_200_OK)
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

        order = Order.objects.get_or_create(customer=customer, complete=False)
        shipping_address = ShippingAddress.objects.create(customer=customer, customer_name=full_name, phone_number=phone_number, order=order, region_name=region_name, address=shipping_street, note=shipping_note, payment_type=pay_type)
        order.complete = True
        order.save()
        order = Order.objects.create(customer=customer, complete=False)
    return JsonResponse({'total_quantity':order.get_total_quantity()})
# Create your views here.
