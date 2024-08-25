from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]

class CategoryInline(admin.TabularInline):
    model = Product
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]


admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)

# Register your models here.
