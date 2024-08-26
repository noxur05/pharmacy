from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

def superuser_required(user):
    return user.is_superuser

@login_required
@user_passes_test(superuser_required)
def admin_dashboard(request):
    pass
# Create your views here.
