from . import settings


class AuthorizationMixin(object):
    """
    Mixin for filter queryset according the defined list of backend.

    :keyword filter_backends: filter backend list
    """

    authorization_filter_class = None

    def get_authorization_filter_class(self):
        """Return all available backends"""
        return self.authorization_filter_class

    def get_queryset(self):
        """
        Method that tries to get a filtered queryset from their parent if it has method defined.
        Otherwise get the queryset from de default manager of the model or raise an error.
        """
        try:
            queryset = super().get_queryset()
        except AttributeError:
            from django.core.exceptions import ImproperlyConfigured
            if self.model is not None:
                queryset = self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "{cls} is missing a QuerySet. Define {cls}.model, {cls}.queryset, or override "
                    "{cls}.get_queryset().".format({'cls': self.__class__.__name__})
                )
        # no filter queryset if the user is superuser or staff and has active the correct setting
        if self.full_permission_for_superuser() or self.full_permission_for_staff():
            return queryset
        return self.filter_queryset(queryset)

    def full_permission_for_superuser(self):
        """Return if the user is superuser and has full permission activated."""
        return self.request.user.is_superuser and settings.FULL_PERMISSION_FOR_SUPERUSERS

    def full_permission_for_staff(self):
        """Return if the user is staff and has full permission activated."""
        return self.request.user.is_staff and settings.FULL_PERMISSION_FOR_STAFF

    def filter_queryset(self, queryset):
        """Given a queryset, filter it with whichever filter backend is in use."""
        filter_class = self.get_authorization_filter_class()
        if filter_class:
            queryset = filter_class().filter_queryset(self.request, queryset, self)
        return queryset

