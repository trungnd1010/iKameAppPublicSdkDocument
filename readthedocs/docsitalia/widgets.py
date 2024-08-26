# -*- coding: utf-8 -*-
"""Custom forms widget."""

from dal import autocomplete
from django import forms

from .models import AllowedTag


# pylint: disable=too-many-ancestors
class WhitelistedTaggitSelect2(autocomplete.TaggitSelect2):
    def build_attrs(self, *args, **kwargs):
        attrs = super(WhitelistedTaggitSelect2, self).build_attrs(*args, **kwargs)
        attrs['data-tags'] = 'false'
        return attrs

    def value_from_datadict(self, data, files, name):
        csv_tags = super(WhitelistedTaggitSelect2, self).value_from_datadict(data, files, name)
        tags = set(csv_tags.split(','))
        filtered_tags = tags & set(
            AllowedTag.objects.filter(enabled=True).values_list('name', flat=True),
        )
        return ','.join(filtered_tags)


class VisibleHiddenInput(forms.TextInput):
    template_name = 'docsitalia/widgets/visible_hidden.html'
