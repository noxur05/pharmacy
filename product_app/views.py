from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_language

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from customer_app.views import get_customer
from order_app.models import *
from order_app.serializers import OrderItemSerializer
from like_app.models import *
from .models import *

import google.generativeai as genai
import sys
import queue

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

@api_view(['POST'])
def product(request):
    data = request.data.get('data')
    customer =  get_customer(request)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    product.in_cart = order.products.filter(id=data).exists()
    if product.in_cart:
        orderItem = OrderItem.objects.get(order=order, product_id=data)
        orderItem.delete()
        status_message = 'deleted'
    else:
        orderItem, created = OrderItem.objects.get_or_create(order=order, product_id=data)
        orderItem.save()
        status_message = 'saved'
    categories = ProductCategory.objects.all().prefetch_related('products')
    return Response({'total_quantity':order.get_total_quantity(), 'status':status_message, 'lang':get_language()}, status=status.HTTP_200_OK)

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

languages = {
    'tm':'Turkmen',
    'ru':'Russian',
    'en':'English',
}

@api_view(['POST'])
def ai_response(request):
    current_language = get_language()
    genai.configure(api_key="AIzaSyAK-he57jjZpBr8q-Cdg9cAb8w7jkOyMTI")
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    prompt = request.data.get("data")
    product = get_object_or_404(Product, id=prompt)
    model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

    prompt = f"System: Create a wide description about the given product name in {languages[current_language]} language.\nUser: {product}"
    response = model.generate_content([prompt])
    if response._done and response._result.candidates:
        candidate = response._result.candidates[0]
        content_parts = candidate.content.parts
        generated_text = content_parts[0].text if content_parts else "No text parts available."
    else:
        generated_text = "No candidates available."
    print(generated_text)
    return Response({'description':generated_text}, status=status.HTTP_200_OK)
# Create your views here.
