from django.apps import AppConfig


class FanForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fan_forum'

    def ready(self):
        import fan_forum.signals