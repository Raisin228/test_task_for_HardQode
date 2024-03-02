from django.db import IntegrityError
from django.db.models import Count
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .utils import CustomError
from .config import *


@receiver(post_save, sender=ProductUser)
def add_user_to_group(sender, instance, created, **kwargs):
    """Добавление пользователя в группу после сохранения записи о доступе к продукту"""
    try:
        if created:
            product = instance.product
            user = instance.user
            min_quant_st, max_quant_st = product.min_quant_students, product.max_quant_students
            groups = Group.objects.filter(product=product).annotate(
                num_students=Count('groupstudent')).order_by('-num_students')

            # Проходим по каждой группе и проверяем, можно ли добавить пользователя в группу
            for group in groups:
                now_quant_st = GroupStudent.objects.filter(group=group).count()

                if min_quant_st <= now_quant_st:
                    if now_quant_st < max_quant_st:
                        # Максимально заполняем группы
                        GroupStudent.objects.create(user=user, group=group)
                        break
                else:
                    raise CustomError(not_enough_people)
            else:
                # не хватило мест в сущ.группах
                raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        raise CustomError(not_enough_places)
    except IntegrityError:
        raise CustomError(incorrect_product_creation)


@receiver(post_delete, sender=ProductUser)
def delete_user_from_group(sender, instance, **kwargs):
    """В случае если пользователь был удалён из курса -> убираем его и из группы"""
    user = instance.user
    product = instance.product

    groups = Group.objects.filter(product=product)

    # Проверяем, что группа существует и что пользователь принадлежит этой группе
    for g in groups:
        if g and GroupStudent.objects.filter(group=g, user=user).exists():
            group_student = GroupStudent.objects.get(group=g, user=user)
            group_student.delete()


@receiver(pre_delete, sender=Group)
def delete_users_from_product(sender, instance, **kwargs):
    """Перед тем как удалить группу. Закрываем доступ к продукту у всех участников группы"""
    product = instance.product
    group_students = GroupStudent.objects.filter(group=instance)

    users_to_delete = group_students.values_list('user', flat=True)

    ProductUser.objects.filter(user__in=users_to_delete, product=product).delete()
