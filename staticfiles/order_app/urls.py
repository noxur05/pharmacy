from django.urls import path
from order_app.views import *

app_name="order_app"


urlpatterns = [
    path('cart/', cart, name="cart"),
    path('increase/', quantity_increase, name="quantity-increase"),
    path('decrease/', quantity_decrease, name="quantity-decrease"),
    path('item-remove/', item_remove, name="item-remove"),
    path('order-remove/', order_remove, name="order-remove"),
    path('shipping/', shipping, name='shipping'),
]