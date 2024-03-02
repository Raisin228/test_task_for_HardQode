from rest_framework import serializers

from .models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода основной информации о всех курсах доступных в системе"""
    # кол-во уроков записанных на курсе
    quantity_lessons = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'data_start', 'price', 'min_quant_students',
                  'max_quant_students', 'author', 'quantity_lessons']


class LessonsSerializer(serializers.ModelSerializer):
    """Сериализация информации об уроках по конкретному продукту"""
    class Meta:
        model = Lesson
        fields = '__all__'

