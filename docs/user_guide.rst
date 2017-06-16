.. django-object-authority documentation master file, created by
   sphinx-quickstart on Thu Jun  1 11:27:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _user_guide:

User Guide
==========

1. Include ``django-object-authority`` in your requirements file or install via `pip`
[:ref:`installation` section].

2. Add ``django_object_authority`` to the ``INSTALLED_APPS`` and add
``django_object_authority.backends.ObjectAuthorityBackend`` to the default django ``AUTHENTICATION_BACKENDS``
[:ref:`configuration` section].

3. Define and register the permissions for your models [:ref:`third_party` section].

.. code-block:: python

    # authorization.py
    from django_object_authority import register
    from django_object_authority import BaseUserObjectAuthorization

    from .models import Book, Article


    @register(Book)
    class BookAuthority(BaseUserObjectAuthorization):

        def has_change_permission(self, user, obj):
            return book.author == user

        def has_delete_permission(self, user, obj):
            return False


    @register(Article)
    class ArticleTeamAuthority(BaseUserObjectAuthorization):

        def has_view_permission(self, user, obj):
            return obj.book.team.filter(user=user).exists()

        def has_change_permisssion(self, user, obj):
            return self.has_view_permission(user, obj) or obj.owner == user

        def has_delete_permission(self, user, obj):
            return obj.owner == user


4. Define your CRUD base views for check user permissions.

.. code-block:: python

    # base_views.py
    from django.core.exceptions import PermissionDenied
    from django.db import models
    from django.views import generic


    class ViewMixin(object):

        def get_codename(self, perm):
            return '{}.{}_{}'.format(self.model._meta.app_label, perm, self.model._meta.model_name)

        def has_view_permission(self, request, obj=None):
            return request.user.has_perm(self.get_codename('view'), obj)


        def has_change_permission(self, request, obj=None):
            return request.user.has_perm(self.get_codename('change'), obj)

        def has_add_permission(self, request):
            return request.user.has_perm(self.get_codename('add'), obj)

        def has_delete_permission(self, request, obj=None):
            return request.user.has_perm(self.get_codename('delete'), obj)

    class CreateBaseView(ViewMixin, generic.CreateView):
        ...

        def get(self, request, *args, **kwargs):
            if not self.has_add_permission(self.request, None):
                raise PermissionDenied
            return super(CreateModelView, self).get(request, *args, **kwargs)


    class RetrieveBaseView(ViewMixin, generic.DetailView):
        ...

        def get_object(self):
            obj = super(BaseDetailView, self).get_object()
            if not self.has_add_permission(self.request, obj):
                raise PermissionDenied
            return obj


    class UpdateBaseView(ViewMixin, generic.UpdateView):
        ...

        def get_object(self):
            obj = super(BaseDetailView, self).get_object()
            if not self.has_change_permission(self.request, obj):
                raise PermissionDenied
            return obj


    class DeleteBaseView(ViewMixin, generic.UpdateView):
        ...

        def get_object(self):
            obj = super(BaseDetailView, self).get_object()
            if not self.has_delete_permission(self.request, obj):
                raise PermissionDenied
            return obj


    class ListBaseView(ViewMixin, generic.ListView):
        ...

        def dispatch(self, request, *args, **kwargs):
            if not self.has_view_permission(self.request):
                raise PermissionDenied
            return super(ListModelView, self).dispatch(request, *args, **kwargs)


5. Create som custom permission for after filtering [:ref:`commands` section].

.. code-block:: python

    python manage.py create_update_permissions -a main -m book -n my_team


6. Define your filter class for accurate list according the authorization over each element
[:ref:`mixins` section].

.. code-block:: python

    # authorization_filters.py
    class BookAuthorityFilter(AuthorityBaseFilter):
        permission_codes = ('my_team', )

        def filter_by_my_team(self, queryset, user):
            return queryset.filter(team=user.team)


7. Custom your list views to filter queryset according the permissions.

.. code-block:: python

    # views.py
    from django_object_authority.mixins import AuthorizationMixin
    from .base_views import ListBaseView

    class BookListView(AuthorizationMixin, ListBaseView):
        authorization_filter_class = BookAuthorityFilter
