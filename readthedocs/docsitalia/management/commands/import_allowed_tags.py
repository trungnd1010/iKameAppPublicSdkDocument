"""Command to sync allowed tags."""
from django.core.management.base import BaseCommand

from readthedocs.docsitalia.models import AllowedTag
from readthedocs.docsitalia.tags_vocabulary import BASE_TAGS


class Command(BaseCommand):
    help = "Sync allowed tags on the database with the python one."

    def handle(self, *args, **options):
        for tag in BASE_TAGS:
            AllowedTag.objects.get_or_create(name=tag.lower(), defaults={'enabled': True})
