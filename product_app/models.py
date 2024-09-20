from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import get_language

from PIL import Image
import os
import io

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=150, null=True)
    category_name_ru = models.CharField(max_length=150, null=True)
    category_name_tm = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.category_name
    
    def get_translated_category(self):
        current_language = get_language()
        if current_language == "tm":
            return self.category_name_tm
        if current_language == "ru":
            return self.category_name_ru
        else:
            return self.category_name
        return self.category_name
    
class Product(models.Model):
    category_name = models.ManyToManyField(ProductCategory, related_name="products")
    product_name = models.CharField(null=True, max_length=100)
    product_name_ru = models.CharField(null=True, max_length=100)
    product_name_tm = models.CharField(null=True, max_length=100)

    product_description = models.TextField(null=True)
    product_description_ru = models.TextField(null=True)
    product_description_tm = models.TextField(null=True)
    original_price = models.FloatField(null=True)
    sale_price = models.FloatField(null=True)
    stock = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        categories = ', '.join([category.category_name for category in self.category_name.all()])
        return f"{self.product_name} ({categories})"

    def get_translated_description(self):
        current_language = get_language()
        if current_language == "tm":
            return self.product_description_tm
        if current_language == "ru":
            return self.product_description_ru
        return self.product_description

    def get_translated_name(self):
        current_language = get_language()
        if current_language == "tm":
            return self.product_name_tm
        if current_language == "ru":
            return self.product_name_ru
        return self.product_name


        
class ProductImage(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True)
    image = models.ImageField(upload_to='media', null=True)

    def __str__(self):
        return str(self.product_name) + ' ' + str(self.image)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def save(self, *args, **kwargs):
        if self.image:
            # Convert image to WebP format
            image_file = self.image
            image = Image.open(image_file)
            webp_image = io.BytesIO()
            image.save(webp_image, format='WebP')
            webp_image.seek(0)
            
            webp_filename = f'{self.image.name.rsplit(".", 1)[0]}.webp'
            self.image.save(webp_filename, io.BytesIO(webp_image.read()), save=False)
            
        super().save(*args, **kwargs)

@receiver(pre_delete, sender=ProductImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)
            print('removed')
        else:
            print('error accured')

@receiver(pre_save, sender=ProductImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = ProductImage.objects.get(pk=instance.pk).image
    except ProductImage.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# Create your models here.
