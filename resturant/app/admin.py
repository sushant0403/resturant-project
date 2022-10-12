from django.contrib import admin
from .models import * 
# Register your models here.


class Dish_galleryInline(admin.TabularInline):
    model = Dish_gallery
    extra = 1 


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class DishAdmin(admin.ModelAdmin):
    list_display=('dish_name','category','modified_date','is_available')
    prepopulated_fields={'slug':('dish_name',)}
    inlines = [Dish_galleryInline,VariationInline]

admin.site.register(Dishes_model,DishAdmin)
admin.site.register(Category)
