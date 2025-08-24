from pathlib import Path

from django.test import TestCase
from rest_framework.test import APIClient

from app.tests.util import with_testuser, save_fixture, with_login, DEFAULT_USER


class AuthApi(TestCase):
    @with_testuser
    def setUp(self):
        self.client = APIClient()

    def test_status_get_unauthenticated(self):
        response = self.client.get('/v1/auth/status/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        assert isinstance(data, dict)

        self.assertEqual(data['username'], None)
        self.assertFalse(data['authenticated'])

        save_fixture(Path("v1/auth/status"), "get-unauthenticated.json", data)

    @with_login
    def test_status_get_authenticated(self):
            response = self.client.get('/v1/auth/status/')
            self.assertEqual(response.status_code, 200)

            data = response.json()
            assert isinstance(data, dict)

            self.assertEqual(data['username'], DEFAULT_USER)
            self.assertTrue(data['authenticated'])

            save_fixture(Path("v1/auth/status"), "get-authenticated.json", data)