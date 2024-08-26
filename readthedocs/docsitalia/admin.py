# -*- coding: utf-8 -*-
"""Admin for the docsitalia app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import PublisherAdminForm
from .models import AllowedTag, Publisher, PublisherProject, ProjectOrder


class PublisherAdmin(admin.ModelAdmin):

    """Admin view for :py:class:`Publisher`."""

    form = PublisherAdminForm
    readonly_fields = ('metadata', 'projects_metadata',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'active'),
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'metadata',
                'projects_metadata',
                'config_repo_name',
                'remote_organization',
            )
        }),
    )
    list_display = ('name', 'remote_organization', 'pub_date',)
    list_filter = ('active',)
    delete_confirmation_template = 'docsitalia/admin/publisher_delete_confirmation.html'
    delete_selected_confirmation_template = 'docsitalia/admin/' \
        'publisher_delete_selected_confirmation_template.html'


class PublisherProjectAdmin(admin.ModelAdmin):

    """Admin view for :py:class:`PublisherProject`."""

    list_filter = ('featured', 'active',)
    list_display = ('name', 'publisher', 'documents', 'pub_date',)
    filter_horizontal = ('projects',)
    delete_confirmation_template = 'docsitalia/admin/publisher_project_delete_confirmation.html'
    delete_selected_confirmation_template = 'docsitalia/admin/' \
        'publisher_project_delete_selected_confirmation_template.html'

    # pylint: disable=no-self-use
    def documents(self, obj):
        """Return the number of linked projects."""
        return obj.projects.count()
    documents.short_description = _('documents')


class AllowedTagAdmin(admin.ModelAdmin):

    """Admin view for :py:class:`AllowedTag`."""

    list_display = ('name', 'enabled')
    list_filter = ('enabled',)


class ProjectOrderAdmin(admin.ModelAdmin):
    list_filter = ('project',)
    search_fields = ('project__name',)
    list_display = ('project', 'priority')
    ordering = ('-priority',)
    list_editable = ('priority', )


admin.site.register(ProjectOrder, ProjectOrderAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(PublisherProject, PublisherProjectAdmin)
admin.site.register(AllowedTag, AllowedTagAdmin)
