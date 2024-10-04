from django.urls import path
from product_app.views import *

app_name="product_app"

urlpatterns = [
    path('category/<int:category_id>/', custom_pills, name="custom-pills"),
    path('add/', product, name='product'),
    path('profile/<int:product_id>', profile, name='profile'),
    path('response/', ai_response, name='ai-response'),

]