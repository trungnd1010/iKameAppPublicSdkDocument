# -*- coding: utf-8 -*-
"""Docs italia api."""

from dal import autocomplete
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from readthedocs.api.v2.serializers import VersionSerializer
from readthedocs.api.v2.views.model_views import ProjectViewSet
from readthedocs.projects.constants import PUBLIC
from ..models import AllowedTag
from ..serializers import (
    DocsItaliaProjectSerializer, DocsItaliaProjectAdminSerializer)


class DocsItaliaProjectViewSet(ProjectViewSet):  # pylint: disable=too-many-ancestors

    """Like :py:class:`ProjectViewSet` but using slug as lookup key."""

    lookup_field = 'slug'
    serializer_class = DocsItaliaProjectSerializer
    admin_serializer_class = DocsItaliaProjectAdminSerializer

    def get_queryset(self):
        """
        Filter projects by tags, publisher and project passed as query parameters.

        e.g. ?tags=tag1,tag2, ?publisher=publisher-slug, ?project=project-slug

        """
        qs = super(DocsItaliaProjectViewSet, self).get_queryset()
        tags = self.request.query_params.get('tags', None)
        if tags:
            tags = tags.split(',')
            qs = qs.filter(tags__slug__in=tags).distinct()
        publisher = self.request.query_params.get('publisher', None)
        if publisher:
            qs = qs.filter(publisherproject__publisher__slug=publisher)
        project = self.request.query_params.get('project', None)
        if project:
            qs = qs.filter(publisherproject__slug=project)
        return qs

    def get_project_for_user_or_404(self, lookup_value):
        """Returns project for user or 404."""
        lookup_query = {self.lookup_field: lookup_value}
        qs = self.get_queryset()

        return get_object_or_404(qs, **lookup_query)

    @action(detail=True)
    def active_versions(self, request, **kwargs):
        """Returns active versions, non private, of a project."""
        project = self.get_project_for_user_or_404(
            kwargs[self.lookup_field]
        )
        versions = project.versions.filter(active=True, privacy_level=PUBLIC)
        return Response({
            'versions': VersionSerializer(versions, many=True).data,
        })


# pylint: disable=too-many-ancestors
class AllowedTagAutocomplete(autocomplete.Select2QuerySetView):

    """Allowed tag listing for autocomplete purpose."""

    def get_queryset(self):
        """Filter and order allowed tags."""
        qs = AllowedTag.objects.filter(enabled=True)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs.order_by('name')
