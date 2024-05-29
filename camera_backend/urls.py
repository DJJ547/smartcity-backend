from django.urls import path, include
from . import views

urlpatterns = [
    path('AddDevice/', views.addDevice),
    path('GetAllDevices/', views.GetALLDevices),
    path('DeleteDevice/', views.deleteDevice),
    path('DisableDevice/', views.disableDevice),
    path('SearchedDevice/', views.searchedDevice),
    path('GetAllIncidences/', views.GetAllIncidences),
    path('StreamVideo/', views.streamVideo),
    path('StopStream/', views.stopStream),
]

