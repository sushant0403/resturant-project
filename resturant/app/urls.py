from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.home, name ="home"),
    path('login/', views.login, name ="login"),
    path('register/', views.register, name ="register"),
]