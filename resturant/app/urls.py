from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name ="home"),
    path("categories/<slug:category_slug>/", views.products_by_categories, name="products_by_categories"),
    path('search_page/', views.search_page, name ="search_page"),
    path('search_page/filter/<str:keyword>', views.search_filter, name ="search_filter"),
    path('dish_detail/<int:id>/', views.dish_detail, name ="dish_detail"),
    path('login/', views.login, name ="login"),
    path('register/', views.register, name ="register"),
    path('logout/', views.logout, name ="logout"),
]