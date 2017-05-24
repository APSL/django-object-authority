from . import settings


class BaseObjectAuthorization(object):

    def has_object_permission(self, user, obj):
        return settings.AUTHORIZE_BY_DEFAULT


class BaseUserObjectAuthorization(BaseObjectAuthorization):

    def has_add_permission(self, user, obj):
        return settings.AUTHORIZE_BY_DEFAULT

    def has_change_permission(self, user, obj):
        return settings.AUTHORIZE_BY_DEFAULT

    def has_delete_permission(self, user, obj):
        return settings.AUTHORIZE_BY_DEFAULT

    def has_view_permission(self, user, obj):
        return settings.AUTHORIZE_BY_DEFAULT
