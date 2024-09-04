from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.apps import apps
from .forms import ADD_OBJECT_LIST

def superuser_required(user):
    return user.is_superuser
    
def global_context(request):
    apps_to_include = ['customer_app', 'product_app', 'order_app', 'like_app', 'ads_app']
    app_models = {}
    for app_name in apps_to_include:
        models = apps.get_app_config(app_name).get_models()
        app_models[app_name] = []
        for model in models:
            in_list = model in ADD_OBJECT_LIST or model.__name__ in ADD_OBJECT_LIST
            app_models[app_name].append({
                'name': model.__name__,
                'in_list': in_list
            })
    return {'app_models':app_models}