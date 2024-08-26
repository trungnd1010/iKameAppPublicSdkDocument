from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from readthedocs.projects.models import Project


class TestProjectQuerysetView(TestCase):
    """Tests for Project Queryset methods."""

    fixtures = ['eric', 'test_data']

    def setUp(self):
        # self.client.login(username='eric', password='test')
        self.pip = Project.objects.get(slug='pip')
        self.version = self.pip.versions.order_by('id').first()
        self.wipe_version_url = reverse('wipe_version', args=[self.pip.slug, self.version.slug])

    def test_user_can_admin(self):
        user_1 = User.objects.get(username='eric')
        self.assertFalse(user_1.is_superuser)
        self.assertTrue(self.pip.users.filter(id=user_1.id).exists())
        qs = Project.objects.user_can_admin(user=user_1)
        self.assertTrue(qs.exists())

        user_2 = User.objects.get(username='tester')
        self.assertFalse(user_2.is_superuser)
        self.assertFalse(self.pip.users.filter(id=user_2.id).exists())
        qs = Project.objects.user_can_admin(user=user_2)
        self.assertFalse(qs.exists())

        user_3 = User.objects.get(username='super')
        self.assertTrue(user_3.is_superuser)
        self.assertFalse(self.pip.users.filter(id=user_3.id).exists())
        qs = Project.objects.user_can_admin(user=user_3)
        self.assertTrue(qs.exists())
