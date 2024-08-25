from django.db import models
from product_app.models import *
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError


from PIL import Image
import os
import io



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True)
    anonym_user = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.anonym_user
        return str(name)
    
class CustomerLocation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    user_address = models.CharField(max_length=245,null=True, blank=True)
    user_lat_long = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} ({self.user_address})"
# Create your models here.
