from django.apps import AppConfig


class PlatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teambuilding.site'
    label = 'site'
    verbose_name = 'Teambuilding Platform'

    def ready(self):
        from . import receivers
