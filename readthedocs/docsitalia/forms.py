# -*- coding: utf-8 -*-
"""Forms for the docsitalia app."""

import logging
from builtins import str # noqa

from django import forms
from django.utils.translation import ugettext_lazy as _

from readthedocs.projects import forms as projects_forms

from .github import get_metadata_for_publisher
from .metadata import PUBLISHER_SETTINGS, PROJECTS_SETTINGS, InvalidMetadata
from .models import Publisher
from .widgets import WhitelistedTaggitSelect2, VisibleHiddenInput

log = logging.getLogger(__name__) # noqa


class PublisherAdminForm(forms.ModelForm):

    """Form for Publisher Admin."""

    def clean(self):
        """Check if the metadata is valid at clean time."""
        super(PublisherAdminForm, self).clean()

        # create the minimal object required for validation. We mock the
        # required RemoteOrganization attributes to reuse the same object.
        slug = self.cleaned_data.get('slug')
        name = self.cleaned_data.get('name')
        publisher = Publisher(slug=slug, name=name)
        publisher.url = ''

        msg = _('Error retrieving {filename}')
        try:
            get_metadata_for_publisher(
                publisher, publisher, PUBLISHER_SETTINGS)
        except InvalidMetadata as exception:
            log.debug(
                'Cannot save publisher: %s', exception)
            raise forms.ValidationError(str(exception))
        except Exception:
            msg = msg.format(filename=PUBLISHER_SETTINGS)
            log.debug(
                'Cannot save publisher: %s', msg)
            raise forms.ValidationError(msg)

        try:
            get_metadata_for_publisher(
                publisher, publisher, PROJECTS_SETTINGS)
        except InvalidMetadata as exception:
            log.debug(
                'Cannot save publisher: %s', exception)
            raise forms.ValidationError(str(exception))
        except Exception:
            msg = msg.format(filename=PROJECTS_SETTINGS)
            log.debug(
                'Cannot save publisher: %s', msg)
            raise forms.ValidationError(msg)

    class Meta:
        model = Publisher
        fields = '__all__'


# pylint: disable=too-many-ancestors
class DocsItaliaUpdateProjectForm(projects_forms.UpdateProjectForm):
    def __init__(self, *args, **kwargs):
        super(DocsItaliaUpdateProjectForm, self).__init__(*args, **kwargs)
        self.fields['tags'].help_text = _('Project tags.')
        # being explicitly declared in form definition (in projects_forms.ProjectExtraForm) we must
        # ovverride explicitly post-init
        self.fields['description'].widget = VisibleHiddenInput()

    class Meta(projects_forms.UpdateProjectForm.Meta):
        widgets = {
            'tags': WhitelistedTaggitSelect2(url='allowedtag-autocomplete'),
            'programming_language': forms.HiddenInput(),
            'project_url': forms.HiddenInput(),
            'name': VisibleHiddenInput(),
            'repo': VisibleHiddenInput(),
            'repo_type': VisibleHiddenInput(),
        }
