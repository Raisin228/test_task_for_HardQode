from django.contrib import admin
from .signals import *


class AbstractClass(admin.ModelAdmin):
    """В этот класс вынесены все методы которые повторяются в остальных моделях
        Стараемся соблюдать принцип DRY!"""

    def get_readonly_fields(self, request, obj=None):
        """Возвращает поля, которые доступны только на чтение"""
        if obj:
            return self.readonly_fields
        return ()

    def has_change_permission(self, request, obj=None) -> bool:
        """Выдаём возможность редактировать объект только его автору"""
        if obj is not None:
            product_id = obj.product_id
            try:
                product = Product.objects.get(pk=product_id)
                return request.user == product.author
            except:
                return False
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Проверяет разрешение на удаление объекта"""
        if obj is not None:
            product = obj.product_id
            if Product.objects.get(id=product).author == request.user:
                return True
        return False


class ProductUserInline(admin.TabularInline):
    """Добавил инлайн форму для отображения списка всех студентов принадлежащих курсу"""
    model = ProductUser
    extra = 1


@admin.register(Product)
class ProductAdminView(AbstractClass):
    """Возможность редактирования продуктов из админки"""
    inlines = (ProductUserInline,)
    list_display = ('title', 'author', 'data_start')
    readonly_fields = ('data_start', 'author')
    fields = ('author', 'title', 'data_start', 'price', 'min_quant_students', 'max_quant_students')

    def get_form(self, request, obj=None, **kwargs):
        """Получаем форму и фильтруем выбор авторов"""
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['author'].queryset = form.base_fields['author'].queryset.filter(id=request.user.id)
        return form

    def has_change_permission(self, request, obj=None):
        """Выдаём возможность редактировать продукт только его автору"""
        if obj is not None and request.user == obj.author:
            return True
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Проверяет разрешение на удаление объекта"""
        # нужно переопределить т.к идёт другой запрос на проверку
        if obj is not None and request.user == obj.author:
            return True
        return False


@admin.register(Lesson)
class LessonAdminView(AbstractClass):
    """Взаимодействие с уроками через админку"""
    list_display = ('title', 'link_to_video')
    readonly_fields = ('product',)
    fields = ('title', 'product', 'link_to_video')

    def get_form(self, request, obj=None, **kwargs):
        """Получаем форму и фильтруем. Оставляем только те данные которые принадлежат этому автору"""
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['product'].queryset = form.base_fields['product'].queryset.filter(
                author_id=request.user.id)
        return form


class GroupStudentInline(admin.TabularInline):
    """Добавил инлайн форму для отображения списка студентов принадлежащих группе"""
    model = GroupStudent
    readonly_fields = ['user']
    can_delete = False
    extra = 0


@admin.register(Group)
class GroupAdminView(AbstractClass):
    """Все группы запущенные на платформу"""
    inlines = (GroupStudentInline,)

    list_display = ('title', 'product')
    readonly_fields = ('product',)
    fields = ('title', 'product')

    def get_form(self, request, obj=None, **kwargs):
        """Получаем форму и фильтруем. Оставляем только те курсы которые принадлежат этому автору"""
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['product'].queryset = form.base_fields['product'].queryset.filter(
                author_id=request.user.id)
        return form
