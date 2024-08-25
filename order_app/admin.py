from django.contrib import admin
from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
        ShippingAddressInline
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingRegion)
admin.site.register(ShippingAddress)
admin.site.register(ShippingConfig)

# Register your models here.
