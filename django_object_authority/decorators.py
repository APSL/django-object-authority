
def register(*models, **kwargs):
    """
    Registers the given model(s) classes into authorization object:

    @authorizations.register(Project)
    class ProjectAuthorization(options.BaseObjectAuthorization):
        pass
    """
    from .authorizations import Authorization, authorization

    def _authorization_wrapper(authorization_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')
        authorization_obj = kwargs.pop('authorization', authorization)
        if not isinstance(authorization_obj, Authorization):
            raise ValueError('site must subclass Authorization')
        authorization_obj.register(models, authorization_class=authorization_class)
        return authorization_class
    return _authorization_wrapper
