from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.apps import apps

def superuser_required(user):
    return user.is_superuser

# @login_required
# @user_passes_test(superuser_required)
def global_context(request):
    apps_to_include = ['customer_app', 'product_app', 'order_app', 'like_app', 'ads_app']
    app_models = {}
    for app_name in apps_to_include:
        models = apps.get_app_config(app_name).get_models()
        app_models[app_name] = [model.__name__ for model in models]
    return {'app_models':app_models}