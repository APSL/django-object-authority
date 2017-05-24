import copy
from importlib import import_module


def autodiscover_authorizations(*args, **kwargs):
    """
    Auto-discover authorization modules and fail silently when not present.
    This forces an import on them to register any authorization classes.

    You may provide a register_to keyword parameter as a way to access a
    registry. This register_to object must have a _registry instance variable
    to access it.
    """
    from django.apps import apps

    register_to = kwargs.get('register_to')
    for app_config in apps.get_app_configs():
        for module_to_search in args:
            # Attempt to import the authorization's module.
            if register_to:
                before_import_registry = copy.copy(register_to._registry)
            try:
                import_module('{}.{}'.format(app_config.name, module_to_search))
            except Exception:
                # Restore last registry on import error occurred
                if register_to:
                    register_to._registry = before_import_registry
