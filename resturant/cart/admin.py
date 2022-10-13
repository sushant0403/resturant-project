from django.contrib import admin
from .models import *
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','date_added')


class Cart_itemAdmin(admin.ModelAdmin):
    list_display=('dish','cart','quantity','is_active')

admin.site.register(Cart,CartAdmin)
admin.site.register(Cart_item,Cart_itemAdmin)