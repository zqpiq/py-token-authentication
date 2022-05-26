from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Genre
from user.tests.test_user_api import create_user


class PublicGenresApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get("http://127.0.0.1:8000/api/cinema/genres/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Genre.objects.create(
            name="Comedy",
        )
        Genre.objects.create(
            name="Drama",
        )
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_genres(self):
        response = self.client.get("/api/cinema/genres/")
        genres = [genre["name"] for genre in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(genres), ["Comedy", "Drama"])

    def test_post_genres(self):
        response = self.client.post(
            "/api/cinema/genres/",
            {
                "name": "Sci-fi",
            },
        )
        db_genres = Genre.objects.all()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(db_genres.count(), 2)
        self.assertEqual(db_genres.filter(name="Sci-fi").count(), 0)

    def test_put_genre(self):
        response = self.client.put(
            "/api/cinema/genres/1/",
            {
                "name": "Sci-fi",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_genre(self):
        response = self.client.delete(
            "/api/cinema/genres/1/",
        )
        db_genres_id_1 = Genre.objects.filter(id=1)
        self.assertEqual(db_genres_id_1.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Genre.objects.create(
            name="Comedy",
        )
        Genre.objects.create(
            name="Drama",
        )
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_genres(self):
        response = self.client.get("/api/cinema/genres/")
        genres = [genre["name"] for genre in response.data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(genres), ["Comedy", "Drama"])

    def test_post_genres(self):
        response = self.client.post(
            "/api/cinema/genres/",
            {
                "name": "Sci-fi",
            },
        )
        db_genres = Genre.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_genres.count(), 3)
        self.assertEqual(db_genres.filter(name="Sci-fi").count(), 1)

    def test_put_genre(self):
        response = self.client.put(
            "/api/cinema/genres/1/",
            {
                "name": "Sci-fi",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_genre(self):
        response = self.client.delete(
            "/api/cinema/genres/1/",
        )
        db_genres_id_1 = Genre.objects.filter(id=1)
        self.assertEqual(db_genres_id_1.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
