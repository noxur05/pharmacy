from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from PIL import Image
import os
import io
class Advertisement(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    url = models.URLField(max_length=200, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.title

    def is_current(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

@receiver(post_save, sender=Advertisement)
def deactivate_expired_ads(sender, instance, **kwargs):
    if instance.end_date < timezone.now() and instance.is_active:
        instance.is_active = False
        instance.save()
    if instance.start_date > timezone.now()  and instance.is_active:
        instance.is_active = False
        instance.save()
    if instance.start_date < timezone.now() < instance.end_date  and not instance.is_active:
        instance.is_active = True
        instance.save()
    
class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="images",null=True)
    image = models.ImageField( upload_to='ads/img/', null=True)

    def __str__(self):
        return str(self.advertisement)
    
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

@receiver(pre_delete, sender=AdvertisementImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)
            print('removed')
        else:
            print('error accured')

@receiver(pre_save, sender=AdvertisementImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = AdvertisementImage.objects.get(pk=instance.pk).image
    except AdvertisementImage.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
# Create your models here.
