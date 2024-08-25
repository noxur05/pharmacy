from django.urls import path
from customer_app.views import *

app_name="customer_app"

urlpatterns = [
    path('location/', user_location, name="user-location"),   
]