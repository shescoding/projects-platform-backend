from django.apps import AppConfig


class ScprojectsConfig(AppConfig):
    name = 'scprojects'

    def ready(self):
        import scprojects.signals
