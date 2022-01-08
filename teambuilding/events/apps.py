from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teambuilding.events'

    def ready(self):
        from . import receivers
