__version__ = "0.0.1"


default_app_config = 'django_object_authority.apps.DjangoObjectAuthorityConfig'


__all__ = [
    'register', 'authorization', 'NoAuthorizationRegistered', 'AlreadyAuthorizationRegistered',
    'BaseObjectAuthorization', 'BaseUserObjectAuthorization', 'autodiscover'
]


from .decorators import register
from .loader import autodiscover_authorizations
from .options import BaseObjectAuthorization, BaseUserObjectAuthorization
from .authorizations import authorization, NoAuthorizationRegistered, AlreadyAuthorizationRegistered


def autodiscover():
    autodiscover_authorizations('authorizations', register_to=authorization)

