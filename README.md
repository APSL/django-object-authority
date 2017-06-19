# Django object authority

**Package to authorize actions over concrete object instances.**

[![travis-image]][travis]
[![pypi-image]][pypi]
[![docs-image]][docs]


## Overview

Django provides an authentication system to authorize users to create, modify or delete models.
The user can perform this action on any element of the class in which it has such permissions.
This package extends these permissions and adds read permissions.

The main function of it is to control the access on specific elements for a concrete action.


## Documentation

Online documentation is available at [http://django-object-authority.readthedocs.io](http://django-object-authority.readthedocs.io/en/latest/)


## Features

* New authentication backend for Django apps.
* New authentication backend for Django rest framework.
* Mechanism to auto-register object permissions.
* Mixin to use in list views that filter your queryset according an authorization filter.
* Per user permissions based filters.
* Command to create custom permission of application and/or specific models.


## Installation

Install using pip:

    $ pip install django-object-authority

## Setup

Add to INSTALLED_APPS
```python
INSTALLED_APPS = (
    ...
    'django_object_authority',
)
```

Add the new backend to AUTHENTICATION_BACKENDS
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_object_authority.backends.ObjectAuthorityBackend',
]
```

Register your object permissions

```python
# authorizations.py
@register(SampleModel)
class SampleModelAuthority(ObjectAuthorization):

    def has_object_permission(self, user, obj):
        return obj.owner == user

    def has_delete_permission(self, user, obj):
        return obj.owner == user and not obj.is_editable
```

[travis-image]: https://secure.travis-ci.org/bcanyelles/django-object-authority.svg?branch=master
[travis]: http://travis-ci.org/apsl/django-object-authority?branch=master
[pypi-image]: https://img.shields.io/pypi/v/django-object-authority.svg
[pypi]: https://pypi.python.org/pypi/django-object-authority
[docs-image]: https://readthedocs.org/projects/docs/badge/?version=latest
[docs]: http://django-object-authority.readthedocs.io/en/latest/

