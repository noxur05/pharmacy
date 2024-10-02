from django.urls import path
from ads_app.views import *

app_name="ads_app"

urlpatterns = [
    path('brands/', active_brand_ads, name="brands")
]