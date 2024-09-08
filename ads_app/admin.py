from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import *

class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage

class AdvertisementAdmin(TranslatableAdmin):
    inlines = [
        AdvertisementImageInline
    ]

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(AdvertisementImage)
# Register your models here.
