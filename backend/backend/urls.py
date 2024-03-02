from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .yasg import urlpatterns as documentation

from base_application.views import ProductAPIView, ProductLessonsAPIView

router = routers.DefaultRouter()
router.register(r'products', viewset=ProductAPIView, basename='products-list')

urlpatterns = [
    path('admin/', admin.site.urls),
    # роутер с api
    path('api/', include(router.urls)),
    path('lessons/<int:product_id>/', ProductLessonsAPIView.as_view(), name='lessons-by-product'),
]

urlpatterns += documentation
