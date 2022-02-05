from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teambuilding.tastepurchase'

    def ready(self):
        from . import receivers