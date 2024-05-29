from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('getAllDevices/', views.get_all_devices_data),
    path('getAllIncidents/', views.get_all_devices_data),
    path('updateAllSpeedCongestion/', views.test_update_all_flow_speed_congestions),
    path('updateAllSpeedCongestionToNow/', views.test_update_all_flow_speed_congestions_to_now),
]