from django.urls import path
from admin_app.views import *

app_name="admin_app"

urlpatterns = [
    path('', admin_dashboard, name="admin-dashboard")
]
