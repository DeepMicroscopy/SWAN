from pathlib import Path

from django.test import TestCase
from rest_framework.test import APIClient

from app.models import Study
from app.tests.util import save_fixture, with_login, with_testuser


class StudyApi(TestCase):
    fixtures = ['study.json']

    @with_testuser
    def setUp(self):
        self.client = APIClient()

    def test_list_unauthorized(self):
        response = self.client.get('/v1/studies/')
        self.assertEqual(response.status_code, 403)

        data = response.json()
        assert isinstance(data, dict)

        self.assertIn('detail', data)

        save_fixture(Path("v1/studies"), "list-unauthorized.json", data)

    @with_login
    def test_list_empty(self):
        # user is not in the group and no study allows anonymous access
        Study.objects.update(group=1, anonymous=False)

        response = self.client.get('/v1/studies/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        assert isinstance(data, list)

        self.assertEqual(len(data), 0)

        save_fixture(Path("v1/studies"), "list-empty.json", data)

    @with_login
    def test_list_anonymous(self):
        # user is not in this group, but one study allows anonymous access
        Study.objects.update(group=1)

        response = self.client.get('/v1/studies/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        assert isinstance(data, list)

        self.assertGreater(len(data), 0)

        save_fixture(Path("v1/studies"), "list-anonymous.json", data)

    @with_login
    def test_list_success(self):
        response = self.client.get('/v1/studies/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        assert isinstance(data, list)

        self.assertGreater(len(data), 0)

        save_fixture(Path("v1/studies"), "list-all.json", data)
