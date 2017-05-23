from django.apps import apps, AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


permissions = ('list', 'view', 'add', 'change', 'delete')


class DjangoObjectAuthorityConfig(AppConfig):
    name = 'django_object_authority'
    verbose_name = _("Django object authority")

    def ready(self):
        """Register all available authorization from modules."""
        super().ready()
        self.module.autodiscover()
        # connect to the event for migration command
        post_migrate.connect(create_update_permissions, sender=self)


def create_update_permissions(applications=None, models=None, **kwargs):
    created_perm, updated_perm = 0, 0

    available_models, available_applications = set(), set(apps.all_models.keys())
    if applications:
        available_applications = set(applications) & set(apps.all_models.keys())

    for app in available_applications:
        app_models = set(apps.all_models.get(app).values())
        if models is not None:
            app_models = {model for model_name, model in apps.all_models.get(app).items() if model_name in set(models)}
        available_models.update(app_models)

    for model in available_models:
        result = _create_permissions(model)
        created_perm += result[0]
        updated_perm += result[1]

    return created_perm, updated_perm


def _create_permissions(model):
    """Get permission or create it."""
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    created, updated = 0, 0
    for perm in permissions:
        kwargs = {
            'codename': "{}_{}".format(perm, model._meta.model_name),
            'content_type': ContentType.objects.get_for_model(model)
        }
        defaults = {'name': "Can {} {}".format(perm, model._meta.verbose_name)}
        obj, _created = Permission.objects.get_or_create(defaults=defaults, **kwargs)

        # count number of permission has created
        if _created:
            created += 1
        else:
            updated += 1

    return created, updated
