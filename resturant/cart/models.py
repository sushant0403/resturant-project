from django.db import models
from django.contrib.auth.models import User
from app.models import *


# Create your models here.

class Cart(models.Model):

    cart_id     = models.CharField(max_length=250,blank=True)
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class Cart_item(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)
    dish        = models.ForeignKey(Dishes_model, on_delete=models.CASCADE, blank = True, null = True)
    variation   = models.ManyToManyField(Variation, blank = True, null = True)
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank = True)
    quantity    = models.IntegerField(blank = True, null = True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.dish.dish_name