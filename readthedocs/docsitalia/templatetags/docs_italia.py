"""Template tags for docs italia app."""

from django import template
from taggit.models import Tag

from readthedocs.core.resolver import resolve

from ..models import PublisherProject


register = template.Library()


@register.filter
def get_publisher_project(slug):
    """get a publisher project from the slug."""
    try:
        return PublisherProject.objects.get(slug=slug)
    except PublisherProject.DoesNotExist:
        return slug


@register.filter
def get_project_tag(slug):
    """Get tag from the slug."""
    try:
        return Tag.objects.get(slug=slug)
    except Tag.DoesNotExist:
        return slug


@register.simple_tag(name="doc_url_patched")
def make_document_url(project, version=None, page=''):
    """Create the full document URL and appends index.html if root."""
    if not project:
        return ""
    url = resolve(project=project, version_slug=version, filename=page)
    if url.endswith('/'):
        url = '%sindex.html' % url
    return url


@register.simple_tag
def url_replace_append(request, field, value):
    """Append a value to the GET dictionary and return it urlencoded."""
    dict_ = request.GET.copy()
    dict_.appendlist(field, value)
    return dict_.urlencode()


@register.simple_tag
def url_replace_pop(request, field, value):
    """Remove a value from the GET dictionary and return it urlencoded."""
    dict_ = request.GET.copy()
    list_ = dict_.pop(field)
    dict_.setlist(field, [v for v in list_ if v != value])
    return dict_.urlencode()
