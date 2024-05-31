from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('addDevice/', views.add_device),
    path('deleteDevice/', views.delete_device),
    path('searchedDevice/', views.get_searched_devices),
    path('disableDevice/', views.disable_device),
    
    path('getAllDevices/', views.get_all_devices_data),
    path('getAllCongestions/' ,views.get_all_congestions_data),
    path('getFlowSpeed/', views.get_flow_speed_for_one_device),
    
    path('updateAllSpeedCongestion/', views.update_all_flow_speed_congestions),
    path('updateAllSpeedCongestionToNow/', views.test_update_all_flow_speed_congestions_to_now),
]