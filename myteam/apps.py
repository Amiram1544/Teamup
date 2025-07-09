from django.apps import AppConfig


class MyteamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myteam'

    def ready(self):
        import myteam.signals