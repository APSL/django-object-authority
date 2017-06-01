.. django-object-authority documentation master file, created by
   sphinx-quickstart on Thu Jun  1 11:27:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _overview:

.. _django-object-permission: https://pypi.python.org/pypi/django-object-permissions
.. _django-guardian: https://pypi.python.org/pypi/django-guardian
.. _django-authority: https://pypi.python.org/pypi/django-authority
.. _dry-rest-permissions: https://github.com/dbkaplan/dry-rest-permissions
.. _Django: https://docs.djangoproject.com/en/1.11/topics/auth/

Overview
========

Django provides an authentication system to authorize users to create, modify or delete objects of a type, that is,
the user can perform this action on any element of the class in which it has such permissions.
This package extends these permissions and adds read permissions.

The main function of the same is to control the access on specific elements for a concrete action.


Features
--------

1. New authentication backend for django apps.
2. New authentication backend for django rest framework.
3. Mechanism to auto-register object permissions.
4. Mixin to use in list views that filter your queryset according an authorization filter.
5. Base filter makes you easier filter your queryset according user's permissions.
6. Command to create custom permission of application and/or specific models.


Inspiration
-----------

This package is base on the default implementation of `Django`_ authentication.

There are some other plugins like `django-object-permission`_, `django-guardian`_, `django-authority`_.
Another framework has inspired in this development has been `dry-rest-permissions`_.
