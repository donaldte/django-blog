import contextlib
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SubscriptionsConfig(AppConfig):
    name = "my_blog_saas.subscriptions"
    verbose_name = _("Subscriptions")

    def ready(self):
        with contextlib.suppress(ImportError):
            import my_blog_saas.subscriptions.signals  # noqa
