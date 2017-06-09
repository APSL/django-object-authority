"""
Settings for Django object authority are all namespaced in the OBJECT_AUTHORITY setting.
For example your project's `settings.py` file might look like this:

OBJECT_AUTHORITY_AUTHORIZE_BY_DEFAULT = True
OBJECT_AUTHORITY_FULL_PERMISSION_FOR_STAFF = True
OBJECT_AUTHORITY_FULL_PERMISSION_FOR_SUPERUSERS = True
"""

from django.conf import settings

AUTHORIZE_BY_DEFAULT = getattr(settings, 'OBJECT_AUTHORITY_AUTHORIZE_BY_DEFAULT', True)
FULL_PERMISSION_FOR_STAFF = getattr(settings, 'OBJECT_AUTHORITY_FULL_PERMISSION_FOR_STAFF', False)
FULL_PERMISSION_FOR_SUPERUSERS = getattr(settings, 'OBJECT_AUTHORITY_FULL_PERMISSION_FOR_SUPERUSERS', True)
CHECK_PERMISSION_CLASS_BY_DEFAULT = getattr(settings, 'OBJECT_AUTHORITY_CHECK_PERMISSION_CLASS_BY_DEFAULT', True)

# Settings applied on post migrations to create permission only for specified apps and models
# or for all models of all installed apps.

PERMISSION_FOR_MODELS = getattr(settings, 'OBJECT_AUTHORITY_PERMISSION_FOR_MODELS', None)
PERMISSION_FOR_APPLICATIONS = getattr(settings, 'OBJECT_AUTHORITY_PERMISSION_FOR_APPLICATIONS', None)


# Default permissions that will be create for models specified before.
DEFAULT_PERMISSIONS = ('view', 'add', 'change', 'delete')
