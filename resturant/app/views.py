from django.shortcuts import render
from .models import *
from django.db.models import Q

# Create your views here.

def home(request):
    dishes = Dishes_model.objects.all()

    context = {
        'dishes': dishes
    }
    return render(request,'pages/home.html', context)

def search_page(request):
    if 'query' in request.GET:
        keyword = request.GET["query"]
        if keyword:
            dishes = Dishes_model.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(slug__icontains=keyword) | Q(dish_name__icontains=keyword))
            product_count   = dishes.count()
    else: 
        dishes = None

    context = {
        'dishes': dishes,
        'product_count': product_count
    }
    return render(request,'pages/search_page.html', context)

def dish_detail(request, id):
    dish  = Dishes_model.objects.get(id=id)
    reviews = ReviewRating.objects.all().filter(dish=dish)
    photos = Dish_gallery.objects.all().filter(dish=dish)
    context = {
        'dish': dish,
        'reviews': reviews,
        'photos': photos
    }
    return render(request,'pages/dish_detail.html', context)

def login(request):
    return render(request,'pages/login.html')

def register(request):
    return render(request,'pages/register.html')