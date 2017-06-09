from .authorizations import authorization, NoAuthorizationRegistered, AlreadyAuthorizationRegistered
from .decorators import register
from .filters import AuthorityBaseFilter, BaseFilter
from .loader import autodiscover_authorizations
from .mixins import AuthorizationMixin
from .options import BaseObjectAuthorization, BaseUserObjectAuthorization


__version__ = "0.0.5"


default_app_config = 'django_object_authority.apps.DjangoObjectAuthorityConfig'


__all__ = [
    'AuthorityBaseFilter', 'AlreadyAuthorizationRegistered', 'AuthorizationMixin', 'BaseFilter',
    'BaseObjectAuthorization', 'BaseUserObjectAuthorization', 'NoAuthorizationRegistered', 'authorization',
    'autodiscover', 'register',
]


def autodiscover():
    autodiscover_authorizations('authorizations', register_to=authorization)
