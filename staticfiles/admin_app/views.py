from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.forms import modelformset_factory, modelform_factory
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from .context_processors import superuser_required
from .forms import *

@login_required
@user_passes_test(superuser_required)
def admin_dashboard(request):
    apps_to_include = ['customer_app', 'product_app', 'order_app', 'like_app', 'ads_app']

    selected_model_name=request.GET.get("model")
    selected_model_form = MODEL_FORM_MAP.get(selected_model_name)

    model_class = selected_model_form()._meta.model
    in_list = model_class in ADD_OBJECT_LIST
    model_name = {
        selected_model_name: {
            'in_list':in_list
        }
    }
    selected_model_fields = []
    selected_model_objects = []
    form_field_names = [field_name for field_name in selected_model_form().fields]
    
    model_class = selected_model_form()._meta.model
    
    model_objects = model_class.objects.all()

    return render(request, 'admin_panel.html', {
        'model_name':model_name,
        'selected_model_field':form_field_names,
        'selected_model_objects':model_objects,
     })

@login_required
@user_passes_test(superuser_required)
def main(request):
    return render(request, 'admin_panel.html')

@user_passes_test(superuser_required)
def add_object(request):
    if request.method == 'GET':
        selected_model_name = request.GET.get("add-object")
    elif request.method == 'POST':
        selected_model_name = request.POST.get("selected_model_name")
    
    selected_model_form = MODEL_FORM_MAP.get(selected_model_name)
    selected_model_formset = MODEL_FORMSET_MAP.get(selected_model_name)

    if request.method == 'POST':
        if selected_model_formset:
            parent_form = selected_model_form(request.POST)
            child_formset = selected_model_formset(request.POST, request.FILES)
            
            if parent_form.is_valid() and child_formset.is_valid():
                try:
                    parent_instance = parent_form.save()
                    child_formset.instance = parent_instance
                    child_formset.save()
                    return JsonResponse({'message': 'Data saved successfully!'})
                except Exception as e:
                    # return JsonResponse({'message': 'Error saving data', 'error': str(e)}, status=500)
                    pass
            else:
                # errors = {
                #     'parent_form_errors': parent_form.errors.as_json(),
                #     'child_formset_errors': [form.errors.as_json() for form in child_formset.forms]
                # }
                # return JsonResponse({'message': 'Validation errors occurred!', 'errors': errors}, status=400)
                pass
        else:
            parent_form = selected_model_form(request.POST)
            if parent_form.is_valid():
                try:
                    parent_form.save()
                    return JsonResponse({'message': 'Data saved successfully!'})
                except:
                    pass
                # except Exception as e:
                    # return JsonResponse({'message': 'Error saving data', 'error': str(e)}, status=500)
            else:
                pass
                # return JsonResponse({'message': 'Validation errors occurred!', 'errors': parent_form.errors.as_json()}, status=400)
    
    if selected_model_formset:
        parent_form = selected_model_form()
        child_formset = selected_model_formset()
        return render(request, 'inline_object_add.html', {
            'selected_model_name':selected_model_name,
            'parent_form': parent_form,
            'child_formset': child_formset
        })
    else:
        parent_form = selected_model_form()
        return render(request, 'add_object.html', {
            'selected_model_name':selected_model_name,
            'form': parent_form
        })

def edit(request):
    if request.method == 'POST':
        obj_id = request.POST.get('id')
        model = request.POST.get('model')
        selected_model_form = MODEL_FORM_MAP.get(model)
        model_class = selected_model_form()._meta.model
        model_objects = model_class.objects.get(id=obj_id)
        form = selected_model_form(instance=model_objects)
    return render(request, 'edit_object.html', {'form':form})

def edit_object(request, form):
    return render(request, 'edit_object.html')
# Create your views here.
