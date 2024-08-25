from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from customer_app.views import get_customer

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
# Create your views here.
