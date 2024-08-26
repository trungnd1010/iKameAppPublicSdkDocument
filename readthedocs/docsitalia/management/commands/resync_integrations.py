"""Resync webhook integrations for all projects."""

from django.core.management.base import BaseCommand

from readthedocs.oauth.utils import SERVICE_MAP
from readthedocs.integrations.models import Integration
from readthedocs.projects.models import Project


def update_webhook(project, integration, user):
    """
    Update integration service webhook.

    This code was taken from `readthedocs.oauth.utils.update_webhook` and was slightly modified.
    It was copied to not override `update_webhook` from the upstream (`request.user` / `messages`).
    Probably this command will be called only once but changes in the upstream function will
    complicate further development.
    """
    service_cls = SERVICE_MAP.get(integration.integration_type)
    if not service_cls:
        return

    updated = False
    try:
        account = project.remote_repository.account
        service = service_cls(user, account)
        updated, __ = service.update_webhook(project, integration)
    except Project.remote_repository.RelatedObjectDoesNotExist:
        # The project was imported manually and doesn't have a RemoteRepository
        # attached. We do brute force over all the accounts registered for this
        # service
        service_accounts = service_cls.for_user(user)
        for service in service_accounts:
            updated, __ = service.update_webhook(project, integration)
            if updated:
                break

    project.has_valid_webhook = updated
    project.save()
    return updated


class Command(BaseCommand):

    """Resync all integrations command."""

    help = 'Resync project integrations'

    # pylint: disable=too-many-branches
    def handle(self, *args, **options):
        """handle command."""
        integrations = Integration.objects.all()

        for integration in integrations:
            user = integration.project.users.first()

            updated = update_webhook(
                project=integration.project,
                integration=integration,
                user=user,
            )
            if not updated:
                print(
                    "Webhook Integration update for project {} failed".format(
                        integration.project.name
                    )
                )
