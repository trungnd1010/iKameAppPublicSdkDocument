"""Build and Version QuerySet classes."""

from django.db import models

from readthedocs.core.utils.extend import SettingsOverrideObject
from readthedocs.projects import constants


__all__ = ['VersionQuerySet', 'BuildQuerySet', 'RelatedBuildQuerySet']


class VersionQuerySetBase(models.QuerySet):

    """Versions take into account their own privacy_level setting."""

    use_for_related_fields = True

    def _add_user_repos(self, queryset, user):
        if user.has_perm('builds.view_version'):
            return self.all()
        if user.is_authenticated:
            projects_pk = user.projects.all().values_list('pk', flat=True)
            user_queryset = self.filter(project__in=projects_pk)
            queryset = user_queryset | queryset
        return queryset

    def public(self, user=None, project=None, only_active=True):
        queryset = self.filter(privacy_level=constants.PUBLIC)
        if user:
            queryset = self._add_user_repos(queryset, user)
        if project:
            queryset = queryset.filter(project=project)
        if only_active:
            queryset = queryset.filter(active=True)
        return queryset.distinct()

    def protected(self, user=None, project=None, only_active=True):
        queryset = self.filter(
            privacy_level__in=[constants.PUBLIC, constants.PROTECTED],
        )
        if user:
            queryset = self._add_user_repos(queryset, user)
        if project:
            queryset = queryset.filter(project=project)
        if only_active:
            queryset = queryset.filter(active=True)
        return queryset.distinct()

    def private(self, user=None, project=None, only_active=True):
        queryset = self.filter(privacy_level__in=[constants.PRIVATE])
        if user:
            queryset = self._add_user_repos(queryset, user)
        if project:
            queryset = queryset.filter(project=project)
        if only_active:
            queryset = queryset.filter(active=True)
        return queryset.distinct()

    def api(self, user=None, detail=True):
        if detail:
            return self.public(user, only_active=False)

        queryset = self.none()
        if user:
            queryset = self._add_user_repos(queryset, user)
        return queryset.distinct()

    def for_project(self, project):
        """Return all versions for a project, including translations."""
        return self.filter(
            models.Q(project=project) |
            models.Q(project__main_language_project=project),
        )


class VersionQuerySet(SettingsOverrideObject):
    _default_class = VersionQuerySetBase


class BuildQuerySetBase(models.QuerySet):

    """
    Build objects that are privacy aware.

    i.e. they take into account the privacy of the Version that they relate to.
    """

    use_for_related_fields = True

    def _add_user_repos(self, queryset, user=None):
        if user.has_perm('builds.view_version'):
            return self.all()
        if user.is_authenticated:
            projects_pk = user.projects.all().values_list('pk', flat=True)
            user_queryset = self.filter(project__in=projects_pk)
            queryset = user_queryset | queryset
        return queryset

    def public(self, user=None, project=None):
        queryset = self.filter(version__privacy_level=constants.PUBLIC)
        if user:
            queryset = self._add_user_repos(queryset, user)
        if project:
            queryset = queryset.filter(project=project)
        return queryset.distinct()

    def api(self, user=None, detail=True):
        if detail:
            return self.public(user)

        queryset = self.none()
        if user:
            queryset = self._add_user_repos(queryset, user)
        return queryset.distinct()


class BuildQuerySet(SettingsOverrideObject):
    _default_class = BuildQuerySetBase


class RelatedBuildQuerySetBase(models.QuerySet):

    """For models with association to a project through :py:class:`Build`."""

    use_for_related_fields = True

    def _add_user_repos(self, queryset, user=None):
        if user.has_perm('builds.view_version'):
            return self.all()
        if user.is_authenticated:
            projects_pk = user.projects.all().values_list('pk', flat=True)
            user_queryset = self.filter(build__project__in=projects_pk)
            queryset = user_queryset | queryset
        return queryset

    def public(self, user=None, project=None):
        queryset = self.filter(build__version__privacy_level=constants.PUBLIC)
        if user:
            queryset = self._add_user_repos(queryset, user)
        if project:
            queryset = queryset.filter(build__project=project)
        return queryset.distinct()

    def api(self, user=None):
        return self.public(user)


class RelatedBuildQuerySet(SettingsOverrideObject):
    _default_class = RelatedBuildQuerySetBase
    _override_setting = 'RELATED_BUILD_MANAGER'
