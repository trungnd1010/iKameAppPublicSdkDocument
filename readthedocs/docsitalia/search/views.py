"""Api for the docsitalia app."""

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search
from rest_framework import generics, serializers

from readthedocs.builds.constants import LATEST

from .documents import quicksearch_index


class SearchSerializer(serializers.Serializer):  # pylint: disable=abstract-method

    """Serializer with basic information for search endpoint."""

    model = serializers.CharField()
    link = serializers.URLField()
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        """Return item text."""
        return obj.meta.highlight.text[0]


class QuickSearchAPIView(generics.ListAPIView):

    """Main entry point for quick search using Elasticsearch."""

    pagination_class = None
    serializer_class = SearchSerializer

    def get_queryset(self):
        """
        Return Elasticsearch DSL Search object instead of Django Queryset.

        Django Queryset and elasticsearch-dsl ``Search`` object is similar pattern.
        So for searching, its possible to return ``Search`` object instead of queryset.
        The ``filter_backends`` and ``pagination_class`` is compatible with ``Search``
        """
        # Validate all the required params are there
        query = self.request.query_params.get('q', '')
        model = self.request.query_params.get('model')
        version = self.request.query_params.get('version', LATEST)
        using = Elasticsearch(**settings.ELASTICSEARCH_DSL['default'])
        search = Search(
            index=f'{quicksearch_index}',
            using=using,
        ).filter(
            Q(
                'terms', model=['progetto', 'amministrazione']
            ) | (
                Q('term', model='documento') & Q('term', version=version)
            )
        ).query('match', text=query).highlight(
            'text', pre_tags=['<mark>'], post_tags=['</mark>'], fragment_size=100
        )
        if model:
            search = search.filter('term', model=model)
        return search[0:10]
