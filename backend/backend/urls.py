from django.contrib import admin
from django.urls import path
from .yasg import urlpatterns as documentation

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += documentation
