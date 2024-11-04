import contextlib
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentsConfig(AppConfig):
    name = "my_blog_saas.comments"
    verbose_name = _("Comments")
    
    def ready(self):
        with contextlib.suppress(ImportError):
            import my_blog_saas.comments.signals