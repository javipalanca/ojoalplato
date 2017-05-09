from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'ojoalplato.blog'
    verbose_name = 'Blog'

    def ready(self):
        import ojoalplato.blog.signals
