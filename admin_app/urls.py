from django.urls import path
from admin_app.views import *

app_name="admin_app"

urlpatterns = [
    path('', main, name="main"),
    path('add/', add_object, name="add-object"),
    path('edit/', edit, name="edit"),
    path('delete/', delete, name="delete"),
    path('login/', user_login, name="login"),
    path('dashboard/', admin_dashboard, name="admin-dashboard")
]
