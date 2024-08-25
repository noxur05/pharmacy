from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from product_app.models import *
from customer_app.models import *

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    total_items_price = models.FloatField(null=True)
    total_price = models.FloatField(null=True)

    def __str__(self):
        return str(self.customer)
    
    def get_total_quantity(self):
        return sum(item.quantity for item in self.orderitems.all())

    def get_total_price(self):
        total = sum(item.get_total_item_price() for item in self.orderitems.all())
        shipping_price = ShippingConfig.get_solo().shipping_price 
        total += shipping_price
        self.total_price = total
        self.save()
    
        return total

    def get_total_items_price(self):
        total = sum(item.get_total_item_price() for item in self.orderitems.all())
        self.total_items_price = total
        self.save()
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name="orderitems" ,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.product} - {self.order}"
    
    def get_total_item_price(self):
        return self.product.sale_price * self.quantity
class ShippingRegion(models.Model):
    region_name = models.CharField(max_length=235)

    def __str__(self):
        return self.region_name
    

CASH = 'cash'
CARD = 'card'
    
PAYMENT_CHOICES = [
    (CASH, 'Cash'),
    (CARD, 'Card'),
]

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    region_name = models.ForeignKey(ShippingRegion, on_delete=models.SET_NULL, null=True )
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default=CASH, null=True)
    note = models.TextField(null=True, blank=True)

class ShippingConfig(models.Model):
    shipping_price = models.FloatField(default=20.00)  # Default price

    def save(self, *args, **kwargs):
        if not self.pk and ShippingConfig.objects.exists():
            raise ValidationError("Only one instance of ShippingConfig is allowed.")
        super().save(*args, **kwargs)

    @staticmethod
    def get_solo():
        return ShippingConfig.objects.first()

    def __str__(self):
        return f"Shipping Price: {self.shipping_price}"


# Create your models here.
