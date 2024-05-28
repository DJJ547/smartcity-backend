from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('getAllData/', views.get_all_data),
    path('updateAllSpeed/', views.test_update_all_speed),
]