from django.db import models

from product_app.models import *
from customer_app.models import *

class Like(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='LikeItem')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.customer)
    
    def save(self, *args, **kwargs):
        if not self.id and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)
    
    
class LikeItem(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes", null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.product} - {self.like} - {self.created_at}"
    
    def save(self, *args, **kwargs):
        if not self.id and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

# Create your models here.
