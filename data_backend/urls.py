from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('getAllDevices/' ,views.get_all_devices_data),
    path('getAllIncidents/' ,views.get_all_incidents_data),
    path('getAllCongestions/' ,views.get_all_congestions_data),
    
    path('testUpdateIncident/', views.test_update_incidents_in_1hour),
    path('testUpdateIncidentsTilNow/', views.test_update_incidents_from_0am_to_now),
    path('testGetAllIncidents/', views.test_get_all_incidents),
]