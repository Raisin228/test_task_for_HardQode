from django.db.models import Count
from rest_framework import viewsets, generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Product, Lesson, ProductUser
from .serializer import ProductSerializer, LessonsSerializer


# ----------------- API -----------------
class ProductAPIView(viewsets.ModelViewSet):
    """Список всех доступных курсов для преобретения"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']

    def get_queryset(self):
        """Подсчитываем количество уроков в каждом продукте"""
        queryset = super().get_queryset().annotate(quantity_lessons=Count('lesson'))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductLessonsAPIView(generics.ListAPIView):
    """Выдаём список всех уроков если пользователь имеет доступ к курсу"""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonsSerializer
    http_method_names = ['get']

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')

        # Проверяем, есть ли у пользователя доступ к продукту
        user = self.request.user
        if not ProductUser.objects.filter(user_id=user, product_id=product_id).exists():
            raise PermissionDenied("User has no access to this product")

        # Получаем все уроки с указанным product_id
        lessons = Lesson.objects.filter(product_id=product_id)

        return lessons
