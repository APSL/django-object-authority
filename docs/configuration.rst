.. django-object-authority documentation master file, created by
   sphinx-quickstart on Thu Jun  1 11:27:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _configuration:


Configuration
=============

There are two modes of usage the library:

1. As a *mixins* that provide you a set of features.
2. Application that autodiscover your objects permissions to apply them to your _Django_ application.


.. _third_party:


As third party application
~~~~~~~~~~~~~~~~~~~~~~~~~~

First of all you should add `django_object_authority` to you `INSTALLED_APPS` settings.
::

    INSTALLED_APPS = (
        ...
        'rest_framework',
    )


Is needed override `AUTHENTICATION_BACKENDS` setting to add `ObjectAuthorityBackend`.
::

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'django_object_authority.backends.ObjectAuthorityBackend',
    ]


For each model you want to custom the permission level is needed define a `authorizations.py` file and register the
permission `class`.
::

    @register(MyModel)
    class MyModelAuthority(BaseUserObjectAuthorization):

        def has_add_permission(self, user, obj):
            return obj.owner == user


If you don't override all `BaseUserObjectAuthorization` defined methods. The default behaviour is defined as a
setting variable [:ref:`settings` section].

`BaseObjectAuthorization` only implements `has_object_permission` method which check the object permission as default
resource.


.. _mixins:

As *mixins*
~~~~~~~~~~~

You can use it only installing the package [:ref:`installation` section] and include the mixin in your views.
::

    from django.views.generic import ListView
    from django_object_authority.mixins import AuthorizationMixin

    class MyListView(AuthorizationMixin, ListView):
        ...
        authorization_filter_class = MyAuthorityFilter
        ...
