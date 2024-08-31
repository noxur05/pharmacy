from django.urls import path
from admin_app.views import *

app_name="admin_app"

urlpatterns = [
    path('', main, name="main"),
    path('add/', add_object, name="add-object"),
    path('add-inline/', add_inline_object, name="add-inline"),
    path('dashboard/', admin_dashboard, name="admin-dashboard")
]
