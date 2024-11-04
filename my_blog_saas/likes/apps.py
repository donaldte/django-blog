import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LikesConfig(AppConfig):
    name = 'my_blog_saas.likes'
    verbose_name = _('Likes')

    def ready(self):
        with contextlib.suppress(ImportError):
            import my_blog_saas.likes.signals


