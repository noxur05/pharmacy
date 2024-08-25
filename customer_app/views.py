from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
import uuid

def get_customer(request):
    """Helper function to get customer based on authentication or cookies."""
    try:
        return request.user.customer
    except:
        anoUsr = request.COOKIES.get('anoUsr')
        if anoUsr is None:
            anoUsr = str(uuid.uuid4())
            response = HttpResponse()
            response.set_cookie('anoUsr', anoUsr, max_age=31536000)  # Cookie expires in 1 year
        else:
            response = None  # No need to set a new cookie if the anoUsr is already present
        customer, _ = Customer.objects.get_or_create(anonym_user=anoUsr)
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
        print("successs")
        customer_location = CustomerLocation.objects.create(customer=customer, ip_address=user_ip, user_address=user_address, user_lat_long=user_lat_long)
    return render(request, 'basket.html')

# Create your views here.
