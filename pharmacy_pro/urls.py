"""
URL configuration for pharmacy_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.views.static import serve


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('dolandyryjy/', admin.site.urls),
    path('', include('core_app.urls')),
    path('customer/', include('customer_app.urls', namespace="customer_app")),
    path('order/', include('order_app.urls', namespace="order_app")),
    path('product/', include('product_app.urls', namespace="product_app")),
    path('like/', include('like_app.urls', namespace="like_app")),
    path('ads/', include('ads_app.urls', namespace="ads_app")),
    path('admin/', include('admin_app.urls', namespace="admin_app")),
]


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)