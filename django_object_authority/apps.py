from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from .utils import create_update_permissions


class DjangoObjectAuthorityConfig(AppConfig):
    name = 'django_object_authority'
    verbose_name = _("Django object authority")

    def ready(self):
        """Register all available authorization from modules."""
        super().ready()
        self.module.autodiscover()
        # connect to the event for migration command
        post_migrate.connect(create_update_permissions, sender=self)
