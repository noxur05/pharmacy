from django.shortcuts import render
from .models import *
from django.utils import timezone

def active_brand_ads(request):
    now = timezone.now()
    brand_ads = Advertisement.objects.filter(
        is_active=True,
        is_brand=True,
        start_date__lte=now,
        end_date__gte=now
    ).prefetch_related('images')
    return render(request, 'brands.html', {'brand_ads': brand_ads})

# Create your views here.
