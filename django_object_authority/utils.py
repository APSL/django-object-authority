from django.apps import apps
from django.contrib.auth import get_permission_codename
from django_object_authority.settings import DEFAULT_PERMISSIONS


def create_update_permissions(applications=None, models=None, permissions=None, **kwargs):
    created_perm, updated_perm = 0, 0
    available_models, available_applications = set(), set(apps.all_models.keys())
    if applications:
        available_applications = set(applications) & set(apps.all_models.keys())

    for app in available_applications:
        app_models = set(apps.all_models.get(app).values())
        if models is not None:
            app_models = {model for model_name, model in apps.all_models.get(app).items() if model_name in set(models)}
        available_models.update(app_models)

    # Update default permissions with the list specified as parameter
    permissions = DEFAULT_PERMISSIONS if not permissions else list(permissions, ) + list(DEFAULT_PERMISSIONS)

    for model in available_models:
        result = _create_permissions(model, permissions)
        created_perm += result[0]
        updated_perm += result[1]

    return created_perm, updated_perm


def _create_permissions(model, permissions):
    """Get permission or create it."""
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    created, updated = 0, 0
    if permissions is not None:
        for perm in permissions:
            kwargs = {
                'codename': "{}_{}".format(perm, model._meta.model_name),
                'content_type': ContentType.objects.get_for_model(model)
            }
            defaults = {'name': "Can {} {}".format(perm.replace('_', ' '), model._meta.verbose_name)}
            obj, _created = Permission.objects.get_or_create(defaults=defaults, **kwargs)

            # count number of permission has created
            if _created:
                created += 1
            else:
                updated += 1

    return created, updated


def get_full_permission_codename(action, opts):
    """
    Returns the full codename of the permission for the specified action.
    """
    app_label = getattr(opts, 'app_label', '')
    return '{}.{}'.format(app_label, get_permission_codename(action, opts))
