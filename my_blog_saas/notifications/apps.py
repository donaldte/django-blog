import contextlib
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = "my_blog_saas.notifications"
    verbose_name = _("Notifications")

    def ready(self):
        with contextlib.suppress(ImportError):
            import my_blog_saas.notifications.signals  # noqa