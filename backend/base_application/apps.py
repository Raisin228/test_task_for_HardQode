from django.apps import AppConfig


class BaseApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_application'
