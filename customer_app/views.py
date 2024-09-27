from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
import uuid

def get_customer(request):
    if request.user.is_authenticated:
        return request.user.customer
    else:
        anonym_user_id = request.session.get('anonym_user_id')
        
        if anonym_user_id is None:
            anonym_user_id = str(uuid.uuid4())
            request.session['anonym_user_id'] = anonym_user_id
        customer, created = Customer.objects.get_or_create(anonym_user=anonym_user_id)
        return customer

def user_location(request):
    customer = get_customer(request)
    if request.method == 'POST':
        user_ip = request.POST.get('userIp')
        user_city = request.POST.get('userCity')
        user_region = request.POST.get('userRegion')
        user_country = request.POST.get('userCountry')
        user_long = request.POST.get('userLongitude')
        user_lat = request.POST.get('userLatitude')
        user_address = f"{user_city}/{user_region}/{user_country}"
        user_lat_long = f"{user_lat} {user_long}"
        customer_location = CustomerLocation.objects.create(customer=customer, ip_address=user_ip, user_address=user_address, user_lat_long=user_lat_long)
    return render(request, 'basket.html')

# Create your views here.
