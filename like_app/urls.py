from django.urls import path
from like_app.views import *

app_name="like_app"

urlpatterns = [
    path('liked/', like_product, name="like_product"),
    path('', favorite, name="favorite"),
]