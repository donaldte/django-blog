import contextlib
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    name = "my_blog_saas.dashboard"
    verbose_name = _("Dashboard")
    
    def ready(self):
        with contextlib.suppress(ImportError):
            import my_blog_saas.dashboard.signals
