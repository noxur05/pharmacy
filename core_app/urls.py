from django.urls import path
from core_app.views import *

urlpatterns = [
    path('', home, name="home"),
    path('search/', search_pill, name='search-pill'),
    path('test-403/', restricted_view),
    path('test-404/', lambda request: 1/0),
    path('test-500/', server_error_view),
]