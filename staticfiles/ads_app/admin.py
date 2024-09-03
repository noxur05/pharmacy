from django.contrib import admin
from .models import *

class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage

class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [
        AdvertisementImageInline
    ]

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(AdvertisementImage)
# Register your models here.
