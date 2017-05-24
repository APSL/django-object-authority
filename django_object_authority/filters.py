from django_object_authority.utils import get_full_permission_codename


class BaseFilter(object):
    """A base class from which all filter backend classes should inherit."""

    def filter_queryset(self, request, queryset, view):
        """Return a filtered queryset."""
        raise NotImplementedError(".filter_queryset() must be overridden.")


class AuthorityBaseFilter(BaseFilter):
    """
    Project filter backend restrict items on queryset according the user permissions.
    The permissions of who request it are provided for his groups. Note that is required define three specific
    permissions for the model.
    Note that is important check his permission with an specific order (defined on: `permission_codes`).
    """
    permission_codes = ()
    prefix_filter_method = 'filter_by'

    def filter_queryset(self, request, queryset, view):
        """Iterate over `permission_codes` to check and filter according its permission codes."""

        if not self._is_valid():
            raise NotImplementedError("Some of {} methods are not implemented.".format(
                self._get_requied_filter_methods()))

        model = getattr(view, 'model', None)
        for code in self.permission_codes:
            # check permission by codename
            codename = get_full_permission_codename(code, getattr(model, '_meta', None))
            if request.user.has_perm(codename, None):
                # filter by criteria
                filter_method = self._get_filter_method(code)
                if hasattr(self, filter_method):
                    queryset = getattr(self, filter_method)(queryset, request.user)

        return queryset

    def _get_filter_method(self, code):
        """Format the filter method according the current permission code."""
        return '{}_{}'.format(self.prefix_filter_method, code)

    def _get_requied_filter_methods(self):
        """Return all required methods that should be implemented."""
        return [self._get_filter_method(code) for code in self.permission_codes]

    def _is_valid(self):
        """Validating that required methods are implemented."""
        filter_methods = self._get_requied_filter_methods()
        return filter_methods and all(map(lambda method: hasattr(self, method), filter_methods))