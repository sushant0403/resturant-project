from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name ="home"),
    path('search_page/', views.search_page, name ="search_page"),
    path('dish_detail/<int:id>/', views.dish_detail, name ="dish_detail"),
    path('login/', views.login, name ="login"),
    path('register/', views.register, name ="register"),
]