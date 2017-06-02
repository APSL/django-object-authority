import re

from django.contrib.auth.backends import ModelBackend
from django.utils.text import slugify

from . import settings, authorization, NoAuthorizationRegistered, BaseObjectAuthorization


class ObjectAuthorityBackend(ModelBackend):

    def has_perm(self, user_obj, perm, obj=None):
        """Main method wrapper to check permissions."""
        return self.has_object_perm(user_obj, perm, obj)

    def has_object_perm(self, user_obj, perm=None, obj=None):
        """
        Validate permissions for the object specified. If there is not object should be validated before with
        the `contrib.auth.backends.ModelBackend`.

        Is required class permission to has permission over an object of the class.
        permissions: `change` `delete` `view`
        """
        if not user_obj.is_active or user_obj.is_anonymous or not all([perm, obj]):
            return False

        # validation object permission
        obj_permission_label = '_has_perm_cache_{}_{}'.format(slugify(perm), obj.id)
        if not hasattr(user_obj, obj_permission_label):
            setattr(user_obj, obj_permission_label, self._has_object_permissions(user_obj, perm, obj))
        return getattr(user_obj, obj_permission_label)

    def _has_object_permissions(self, user_obj, perm, obj):
        """Gets the user permission for the object.

        By default, allow all staff and superusers do the action:
        Settings configuration:
        * FULL_PERMISSION_FOR_STAFF
        * FULL_PERMISSION_FOR_SUPERUSERS

        Gets the registered permission class linked with the object class and validate for the action specified.
        """
        model = self._get_model(obj)
        assert model is not None, (
            "Object {} must be a `Model` instance to check object permission.".format_map(obj.__class__)
        )

        # check if is superuser or staff to allow the access to the object
        if self._has_permission_as_superuser(user_obj) or self._has_permission_as_staff(user_obj):
            return True

        action = self._get_action(perm, model)
        model_permission = self._get_model_permission_class(model)

        if action:
            action_method_name = "has_{action}_permission".format(action=action)
            if hasattr(model_permission, action_method_name):
                return getattr(model_permission, action_method_name)(user=user_obj, obj=obj)

        # check class permission if CHECK_PERMISSION_CLASS_BY_DEFAULT is True
        if settings.CHECK_PERMISSION_CLASS_BY_DEFAULT:
            return user_obj.has_perm(perm)

        # otherwise check default object permission
        if hasattr(model_permission, 'has_object_permission'):
            return model_permission.has_object_permission(user_obj, obj)

        return False

    def _get_model_permission_class(self, model):
        """
        Gets the permission class registered for the current model.

        Return default `BaseObjectPermission` class if there are no permission classes regitered for the model.
        """
        try:
            return authorization.get(model)()
        except NoAuthorizationRegistered:
            return BaseObjectAuthorization()

    def _get_action(self, perm, model):
        try:
            perm = perm.rsplit('.', 1)[1]
        except IndexError:
            pass
        try:
            return re.sub(r'_{}.*'.format(self._get_model_name(model)), '', perm)
        except (TypeError, IndexError):
            return None

    @staticmethod
    def _get_model(obj):
        return getattr(getattr(obj, '_meta', object()), 'model', None)

    @staticmethod
    def _get_model_name(obj):
        return getattr(getattr(obj, '_meta', object()), 'model_name', '')

    @staticmethod
    def _get_model_label(obj):
        return getattr(getattr(obj, '_meta', object()), 'label', '')

    @staticmethod
    def _has_permission_as_staff(user):
        return getattr(user, 'is_staff', False) and settings.FULL_PERMISSION_FOR_STAFF

    @staticmethod
    def _has_permission_as_superuser(user):
        return getattr(user, 'is_superuser', False) and settings.FULL_PERMISSION_FOR_SUPERUSERS


class DRFAuthorityBackend(ObjectAuthorityBackend):
    """
    A base class permission backend with required methods from `BasePermission` drf class.
    """
    default_action_mapping = {

        # default mapping for APIView subclasses
        'get': 'view',
        'post': 'add',
        'put': 'change',
        'patch': 'change',
        'delete': 'delete',

        # default mapping for GenericViewSet subclasses
        'retrieve': 'view',
        'create': 'add',
        'update': 'change',
        'partial_update': 'change',
        'destroy': 'delete',
    }

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        action = getattr(view, 'action', request.method.lower())
        if action not in self.default_action_mapping:
            return False
        return self.has_perm(request.user, self.default_action_mapping[action], obj)
