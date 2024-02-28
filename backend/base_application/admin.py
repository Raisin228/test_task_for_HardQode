from django.contrib import admin

from .models import Product, Lesson, GroupStudent, Group


@admin.register(Product)
class ProductAdminView(admin.ModelAdmin):
    """Возможность редактирования продуктов из админки"""
    list_display = ('title', 'author', 'data_start')
    readonly_fields = ('data_start', 'author')
    fields = ('author', 'title', 'data_start', 'price', 'min_quant_students', 'max_quant_students')

    def get_form(self, request, obj=None, **kwargs):
        """Получаем форму и фильтруем выбор авторов"""
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['author'].queryset = form.base_fields['author'].queryset.filter(id=request.user.id)
        return form

    def get_readonly_fields(self, request, obj=None):
        """Возвращает поля, которые доступны только на чтение"""
        if obj:
            return self.readonly_fields
        return ()

    def has_change_permission(self, request, obj=None):
        """Выдаём возможность редактировать продукт только его автору"""
        if obj is not None and request.user == obj.author:
            return True
        return False


@admin.register(Lesson)
class LessonAdminView(admin.ModelAdmin):
    """Взаимодействие с уроками через админку"""
    list_display = ('title', 'link_to_video')
    readonly_fields = ('product',)
    fields = ('title', 'product', 'link_to_video')

    def get_form(self, request, obj=None, **kwargs):
        """Получаем форму и фильтруем выбор курсов.
        Сделано потому что автор может выкладывать видео только к своему курсу"""
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['product'].queryset = form.base_fields['product'].queryset.filter(
                author_id=request.user.id)
        return form

    def get_readonly_fields(self, request, obj=None):
        """Возвращает поля которые доступны только на чтение"""
        if not obj:
            return ()
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        """Выдаём возможность редактировать урок только его автору"""
        if obj is not None:
            product_id = obj.product_id
            try:
                product = Product.objects.get(pk=product_id)
                return request.user == product.author
            except:
                return False
        return False


@admin.register(Group)
class GroupAdminView(admin.ModelAdmin):
    """Все группы запущенные на платформу"""
    list_display = ('title', 'product')
    readonly_fields = ('product',)
    fields = ('title', 'product')

    def get_readonly_fields(self, request, obj=None):
        """Возвращает поля которые доступны только на чтение"""
        if not obj:
            return ()
        return self.readonly_fields
