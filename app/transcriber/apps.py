from django.apps import AppConfig


class TranscriberConfig(AppConfig):
    name = 'transcriber'
    def ready(self) -> None:
        import celery
        return super().ready()