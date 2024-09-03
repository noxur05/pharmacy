from django.contrib import admin
from .models import *

class LikeItemInline(admin.TabularInline):
    model = LikeItem

class LikeAdmin(admin.ModelAdmin):
    inlines = [
        LikeItemInline
    ]

admin.site.register(Like, LikeAdmin)
admin.site.register(LikeItem)


# Register your models here.
