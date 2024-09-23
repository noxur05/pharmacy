from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from customer_app.models import *
from order_app.models import *
from product_app.models import *
from like_app.models import *
from ads_app.models import *

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
        fields = "__all__"

class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = "__all__"


class ShippingRegionForm(forms.ModelForm):
    
    class Meta:
        model = ShippingRegion
        fields = ("region_name",)
    
    def __init__(self, *args, **kwargs):
        super(ShippingRegionForm, self).__init__(*args, **kwargs)

        self.fields['region_name'].widget.attrs['class'] = 'form-control'

class ShippingAddressForm(forms.ModelForm):
    
    class Meta:
        model = ShippingAddress
        fields = "__all__"

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)


        self.fields['category_name'].widget.attrs['class'] = 'form-control'
        self.fields['product_name'].widget.attrs['class'] = 'form-control'
        self.fields['product_name_ru'].widget.attrs['class'] = 'form-control'
        self.fields['product_name_tm'].widget.attrs['class'] = 'form-control'
        self.fields['product_description'].widget.attrs['class'] = 'form-control'
        self.fields['product_description_ru'].widget.attrs['class'] = 'form-control'
        self.fields['product_description_tm'].widget.attrs['class'] = 'form-control'
        self.fields['original_price'].widget.attrs['class'] = 'form-control'
        self.fields['sale_price'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['class'] = 'form-control'


class ProductCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ProductCategory
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(ProductCategoryForm, self).__init__(*args, **kwargs)

        self.fields['category_name'].widget.attrs['class'] = 'form-control'
        self.fields['category_name_ru'].widget.attrs['class'] = 'form-control'
        self.fields['category_name_tm'].widget.attrs['class'] = 'form-control'

class ProductImageForm(forms.ModelForm):
    
    class Meta:
        model = ProductImage
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'

class ShippingConfigForm(forms.ModelForm):
    
    class Meta:
        model = ShippingConfig
        fields = ("shipping_price",)

class LikeForm(forms.ModelForm):
    
    class Meta:
        model = Like
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['products'].widget = forms.CheckboxSelectMultiple()

class LikeItemForm(forms.ModelForm):
    
    class Meta:
        model = LikeItem
        fields = "__all__"

class AdvertisementForm(forms.ModelForm):
    
    class Meta:
        model = Advertisement
        fields = ("title", "description", "url", "start_date", "end_date", "is_active", "is_brand",)
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }
    
    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget.attrs['placeholder'] = 'https://example.com/'
        self.fields['start_date'].widget.attrs['class'] = 'form-control'
        self.fields['end_date'].widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['class'] = 'form-control'
        self.fields['is_brand'].widget.attrs['class'] = 'form-control'

class AdvertisementImageForm(forms.ModelForm):
    
    class Meta:
        model = AdvertisementImage
        fields = ("advertisement","image",)

    def __init__(self, *args, **kwargs):
        super(AdvertisementImageForm, self).__init__(*args, **kwargs)

        self.fields['advertisement'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'

class CustomChildFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomChildFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            if 'DELETE' in form.fields:
                form.fields.pop('DELETE')

MODEL_FORM_MAP = {
    'Customer':CustomerForm,
    'CustomerLocation':CustomerLocationForm,
    'Product':ProductForm,
    'ProductImage':ProductImageForm,
    'ProductCategory':ProductCategoryForm,
    'Order':OrderForm,
    'OrderItem':OrderItemForm,
    'ShippingRegion':ShippingRegionForm,
    'ShippingAddress':ShippingAddressForm,
    'ShippingConfig':ShippingConfigForm,
    'Like':LikeForm,
    'LikeItem':LikeItemForm,
    'Advertisement':AdvertisementForm,
    'AdvertisementImage':AdvertisementImageForm,
}
ProductImageFormset = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    formset=CustomChildFormSet,
    extra=1,
)

AdvertisementImageFormset = inlineformset_factory(
    Advertisement,
    AdvertisementImage,
    form=AdvertisementImageForm,
    formset=CustomChildFormSet,
    extra=1,
)

MODEL_FORMSET_MAP = {
    'Product':ProductImageFormset,
    'Advertisement':AdvertisementImageFormset
}

ADD_OBJECT_LIST = [Product, ProductImage, ProductCategory, ShippingRegion, Advertisement, AdvertisementImage]
SHIPPING_REGION_LIST = [ShippingConfig]





