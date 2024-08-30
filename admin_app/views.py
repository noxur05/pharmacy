from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.apps import apps
from .context_processors import superuser_required
from .forms import *

@login_required
@user_passes_test(superuser_required)
def admin_dashboard(request):
    apps_to_include = ['customer_app', 'product_app', 'order_app', 'like_app', 'ads_app']

    selected_model_name=request.GET.get("model")
    selected_model_form = MODEL_FORM_MAP.get(selected_model_name)

    selected_model_fields = []
    selected_model_objects = []
    form_field_names = [field_name for field_name in selected_model_form.fields]
    
    model_class = selected_model_form._meta.model
    
    model_objects = model_class.objects.all()

    return render(request, 'admin_panel.html', {
        'selected_model_name':selected_model_name,
        'selected_model_field':form_field_names,
        'selected_model_objects':model_objects,
     })

@login_required
@user_passes_test(superuser_required)
def main(request):
    return render(request, 'admin_panel.html')

@user_passes_test(superuser_required)
def add_object(request):
    apps_to_include = ['customer_app', 'product_app', 'order_app', 'like_app', 'ads_app']

    selected_model_name=request.GET.get("add-object")

    selected_model_form = MODEL_FORM_MAP.get(selected_model_name)
    print(selected_model_form)

    return render(request, "add_object.html", {'form':selected_model_form})
# Create your views here.
