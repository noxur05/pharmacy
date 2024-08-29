from django.urls import path
from core_app.views import *

urlpatterns = [
    path('', home, name="home"),
    path('search/', search_pill, name='search-pill'),
]