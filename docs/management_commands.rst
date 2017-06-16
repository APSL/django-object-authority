.. django-object-authority documentation master file, created by
   sphinx-quickstart on Thu Jun  1 11:27:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _commands:

Management commands
===================

The library provide a *Django* command line to create or update new permission ``django.contrib.auth.Permission``
instances.

How to use it
~~~~~~~~~~~~~

By default the command creates a new ``Permission`` if it does not exist. Otherwise it will update it.
::

    python manage.py create_update_permissions -n my_custom_permission_1 my_custom_permission_2

This execution will create/update all permissions defined on ``-n`` parameter for each non auto-created [*]_ model of
each registered application.

If you want to filter the applications and/or models for creation/update you can use ``-a`` and/or ``-m`` respective.

Use case
~~~~~~~~

This feature could be very useful to configure your object permission according those *Django* permissions.
::

    @register(MyModel)
    class MyModelAuthority(ObjectAuthorization):

        def has_view_permission(self, user, obj):
            codename = '{}.{}_{}'.format(obj._meta.app_label, 'my_custom_permission_1', obj._meta.model_name))
            return codename in user.get_all_permissions()


.. [*] All models that django creates as a many to many relationship result.