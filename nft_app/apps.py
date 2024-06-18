from django.apps import AppConfig


class NftAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nft_app'

    def ready(self):
        import nft_app.signals
