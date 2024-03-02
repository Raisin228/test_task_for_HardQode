from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL


class Product(models.Model):
    """Модель продукта|онлайн курса"""
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор курса')
    title = models.CharField(max_length=256, verbose_name='Название')
    data_start = models.DateTimeField(verbose_name='Дата запуска')
    price = models.IntegerField(verbose_name='Стоимость', validators=[MinValueValidator(0)])
    min_quant_students = models.IntegerField(default=0,
                                             verbose_name='Минимальное количество студентов в группе',
                                             validators=[MinValueValidator(0), MaxValueValidator(1000)])
    max_quant_students = models.IntegerField(default=10,
                                             verbose_name='Максимальное количество студентов в группе',
                                             validators=[MinValueValidator(0), MaxValueValidator(1000)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductUser(models.Model):
    """Доп. таблица для связи студент <-> доступ к продукту"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = "ProductUser"
        verbose_name = "Студент курса"
        verbose_name_plural = "Студенты курса"


class Lesson(models.Model):
    """Модель урока"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512, verbose_name='Название')
    link_to_video = models.URLField(max_length=2024, verbose_name='Ссылка на видео-материал')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Lesson"
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Group(models.Model):
    """Группа студентов и её базовая конфигурация"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, verbose_name='Название группы')
    product = models.ForeignKey('Product', on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Group"
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"


class GroupStudent(models.Model):
    """Промежуточная таблица. Нужна для связи many to many (Студент <-> Группа)"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        db_table = "GroupStudent"
        verbose_name = "Студент группы"
        verbose_name_plural = "Студенты группы"
        unique_together = ('user', 'group')
