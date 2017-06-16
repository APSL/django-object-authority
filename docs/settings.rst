.. django-object-authority documentation master file, created by
   sphinx-quickstart on Thu Jun  1 11:27:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _settings:

Settings
========

Settings for Django object authority are all namespaced in the *OBJECT_AUTHORITY* setting.
For example your project's `settings.py` file might look like this::

    OBJECT_AUTHORITY_AUTHORIZE_BY_DEFAULT = True


AUTHORIZE_BY_DEFAULT
    Boolean value that define the default behaviour for authorization user object action.

    Default ``True``


AUTHORIZE_ONLY_OBJECTS
    Boolean value for validate *class* permission before validate *object* permissions.

    Default: ``False``


FULL_PERMISSION_FOR_STAFF
    Boolean value to allow all access if the user requester is **staff**.

    Default: ``False``


FULL_PERMISSION_FOR_SUPERUSERS
    Boolean value to allow all access if the user requester is **superuser**.

    Default: ``True``
