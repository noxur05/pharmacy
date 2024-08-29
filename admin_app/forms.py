from django import forms
from customer_app.models import *
from order_app.models import *
from product_app.models import *

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ("user", "name", "email", "phone_number", "anonym_user",)

class CustomerLocationForm(forms.ModelForm):
    
    class Meta:
        model = CustomerLocation
        fields = ("customer","ip_address", "user_address", "user_lat_long",)


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("customer", "total_items_price", "total_price", "complete",)

class OrderItemForm(forms.ModelForm):

    date_added_display = forms.DateTimeField(required=False,
    widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    
    class Meta:
        model = OrderItem
        fields = ("product","order","quantity",)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['date_added_display'].initial = self.instance.date_added

class ShippingRegionForm(forms.ModelForm):
    
    class Meta:
        model = ShippingRegion
        fields = ("region_name",)

class ShippingAddressForm(forms.ModelForm):
    
    class Meta:
        model = ShippingAddress
        fields = ("customer", "customer_name", "phone_number", "order", "region_name", "address", "payment_type", "note")

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ("category_name","product_name", "product_description", "original_price", "sale_price", "stock",)


class ProductCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ProductCategory
        fields = ("category_name",)

class ProductImageForm(forms.ModelForm):
    
    class Meta:
        model = ProductImage
        fields = ("product_name","image",)


MODEL_FORM_MAP = {
    'Customer':CustomerForm(),
    'CustomerLocation':CustomerLocationForm(),
    'Product':ProductForm(),
    'ProductImage':ProductImageForm(),
    'ProductCategory':ProductCategoryForm(),
    'Order':OrderForm(),
    'OrderItem':OrderItemForm(),
    'ShippingRegion':ShippingRegionForm(),
    'ShippingAddress':ShippingAddressForm(),
}




