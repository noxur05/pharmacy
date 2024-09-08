import django_filters
from product_app.models import *
from order_app.models import *
from django import forms

class ProductFilter(django_filters.FilterSet):
    product_name=django_filters.CharFilter(lookup_expr='icontains')

    category_name = django_filters.ModelMultipleChoiceFilter(
        queryset=ProductCategory.objects.all(),
        widget=forms.SelectMultiple,
    )

    min_price = django_filters.NumberFilter(field_name='sale_price', lookup_expr="gte", label="Min Sale Price")
    max_price = django_filters.NumberFilter(field_name='sale_price', lookup_expr="lte", label="Max Sale Price")

    min_stock = django_filters.NumberFilter(field_name='stock', lookup_expr="gte", label="Min Stock")
    max_stock = django_filters.NumberFilter(field_name='stock', lookup_expr="lte", label="Max Stock")

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)

        self.filters['product_name'].field.widget.attrs['class'] = 'form-control '
        self.filters['category_name'].field.widget.attrs['class'] = 'form-control '
        self.filters['sale_price'].field.widget.attrs['class'] = 'form-control'
        self.filters['stock'].field.widget.attrs['class'] = 'form-control'
        self.filters['min_price'].field.widget.attrs['class'] = 'form-control'
        self.filters['max_price'].field.widget.attrs['class'] = 'form-control'
        self.filters['min_stock'].field.widget.attrs['class'] = 'form-control'
        self.filters['max_stock'].field.widget.attrs['class'] = 'form-control'

    class Meta:
        model=Product
        fields = ("product_name", "category_name", "sale_price", "stock",)

"""
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    region_name = models.ForeignKey(ShippingRegion, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(null=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default=CASH, null=True)
    note = models.TextField(null=True, blank=True)
"""
class ShippingAddressFilter(django_filters.FilterSet):
    customer_name=django_filters.CharFilter(lookup_expr='icontains')
    phone_number=django_filters.CharFilter(lookup_expr='icontains')
    address=django_filters.CharFilter(lookup_expr='icontains')
    min_added=django_filters.DateFilter(field_name="date_added", lookup_expr="gte", label="From Date", widget=forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    max_added=django_filters.DateFilter(field_name="date_added", lookup_expr="lte", label="To Date", widget=forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))

    region_name = django_filters.ModelChoiceFilter(
        queryset=ShippingRegion.objects.all(),
        widget=forms.SelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(ShippingAddressFilter, self).__init__(*args, **kwargs)

        self.filters['customer_name'].field.widget.attrs['class'] = 'form-control '
        self.filters['phone_number'].field.widget.attrs['class'] = 'form-control '
        self.filters['address'].field.widget.attrs['class'] = 'form-control'
        self.filters['max_added'].field.widget.attrs['class'] = 'form-control'
        self.filters['min_added'].field.widget.attrs['class'] = 'form-control'
        self.filters['region_name'].field.widget.attrs['class'] = 'form-control'
        self.filters['date_added'].field.widget.attrs['class'] = 'form-control'

    class Meta:
        model=ShippingAddress
        fields = ("customer_name", "phone_number", "address", "region_name", "date_added",)
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'datetime-local'}),
        #     'max_added': forms.DateInput(attrs={'type': 'datetime-local'})
        }

MODEL_FILTER_MAP = {
    'Product':ProductFilter,
    'ShippingAddress':ShippingAddressFilter,
}
