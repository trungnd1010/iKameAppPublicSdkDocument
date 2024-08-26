"""Override RTD URL resolver."""

from django.conf import settings

from readthedocs.core.resolver import ResolverBase


class ItaliaResolver(ResolverBase):

    """
    Custom path resolver for built documentation.

    Resolves to public domain without use of subdomains or /doc/* paths.
    It also takes publisher into account
    """

    def base_resolve_path(self, project_slug, filename, version_slug=None,
                          language=None, private=False, single_version=None,
                          subproject_slug=None, subdomain=None, cname=None):
        """
        Generates the URL for a document according to its project / publisher.

        :param project_slug: project (document) slug
        :param filename: filename
        :param version_slug: version slug
        :param language: language
        :param private: if document is private
        :param single_version: if document has single version
        :param subproject_slug: optional subproject slug
        :param subdomain: optional subdomain
        :param cname: optional subdomain
        :return: string
        """
        from readthedocs.projects.models import Project

        project = Project.objects.get(slug=project_slug)
        base_project = project.publisherproject_set.all().first()

        if not base_project or private:
            return super(ItaliaResolver, self).base_resolve_path(
                project_slug, filename, version_slug,
                language, private, single_version,
                subproject_slug, subdomain, cname
            )

        url = u'/{publisher_slug}/{base_project_slug}/{project_slug}/'

        if subproject_slug:
            url += u'projects/{subproject_slug}/'

        if single_version:
            url += u'{filename}'
        else:
            url += u'{language}/{version_slug}/{filename}'

        return url.format(
            project_slug=project_slug, filename=filename,
            base_project_slug=base_project.slug, publisher_slug=base_project.publisher.slug,
            version_slug=version_slug, language=language,
            single_version=single_version, subproject_slug=subproject_slug,
        )

    def resolve_domain(self, project, private=None):
        """
        Resolve the public domain for the given project.

        :param project: project (document) instance
        :param private: if document is private
        :return: string
        """
        canonical_project = self._get_canonical_project(project)
        domain = canonical_project.domains.filter(canonical=True).first()
        if domain:
            return domain.domain
        return getattr(settings, 'PUBLIC_DOMAIN')

    # pylint: disable=arguments-differ
    def resolve(self, project, require_https=False, filename='', private=None, **kwargs):
        """
        Resolve the complete URL to the provided project (document).

        :param project: project (document) instance
        :param require_https: use https protocol
        :param filename: path to the document file
        :param private: if document is private
        :param kwargs: other kwargs
        :return: string
        """
        require_https = getattr(settings, 'PUBLIC_DOMAIN_USES_HTTPS', False)
        # get readable international slug name if language is not italian
        from readthedocs.docsitalia.utils import get_international_version_slug
        kwargs['version_slug'] = get_international_version_slug(
            project, kwargs.get('language', None), kwargs.get('version_slug', None)
        )
        return super(ItaliaResolver, self).resolve(
            project, require_https=require_https, filename=filename, private=private, **kwargs
        )

    @staticmethod
    def resolve_docsitalia(publisher_slug, pb_project_slug=None, protocol='http'):
        """
        Resolve the complete URL for a publisher or a publisher project.

        :param publisher_slug: the publisher slug
        :param pb_project_slug: the publisher project slug
        :param protocol: http / https protocol
        """
        domain = getattr(settings, 'PRODUCTION_DOMAIN')
        require_https = getattr(settings, 'PUBLIC_DOMAIN_USES_HTTPS', False)
        protocol = 'https' if require_https else 'http'
        if pb_project_slug:
            path = u'{}/{}'.format(publisher_slug, pb_project_slug)
        else:
            path = publisher_slug
        return u'{}://{}/{}'.format(
            protocol,
            domain,
            path
        )
