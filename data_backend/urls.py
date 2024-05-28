from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('updateIncident/', views.test_update_all_incidents),
]