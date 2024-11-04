import contextlib
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    name = "my_blog_saas.blog"
    verbose_name = _("Blog")
    
    def ready(self):
        with contextlib.suppress(ImportError):
            import my_blog_saas.blog.signals
