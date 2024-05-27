from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('getAllData/', views.get_all_data),
    path('updateAllSpeed/', views.update_all_speed),
]