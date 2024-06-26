from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_system.urls')),
    path('dashboard/', include('data_backend.urls')),
    path('iot/', include('iot_backend.urls')),
    path('camera/', include('camera_backend.urls')),
    path('drone/', include('drone_backend.urls')),
]
