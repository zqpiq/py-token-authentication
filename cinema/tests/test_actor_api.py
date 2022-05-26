from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Actor
from user.tests.test_user_api import create_user


class PublicActorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get("http://127.0.0.1:8000/api/cinema/actors/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateActorApiTests(TestCase):
    def setUp(self):
        Actor.objects.create(first_name="George", last_name="Clooney")
        Actor.objects.create(first_name="Keanu", last_name="Reeves")

        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_actors(self):
        response = self.client.get("/api/cinema/actors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actors_full_names = [actor["full_name"] for actor in response.data]
        self.assertEqual(sorted(actors_full_names), ["George Clooney", "Keanu Reeves"])

    def test_post_actors(self):
        response = self.client.post(
            "/api/cinema/actors/",
            {
                "first_name": "Scarlett",
                "last_name": "Johansson",
            },
        )
        db_actors = Actor.objects.all()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(db_actors.count(), 2)
        self.assertEqual(db_actors.filter(first_name="Scarlett").count(), 0)

    def test_get_invalid_actor(self):
        response = self.client.get("/api/cinema/actors/1001/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_actor(self):
        response = self.client.put(
            "/api/cinema/actors/1/",
            {
                "first_name": "George",
                "last_name": "Clooney",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_actor(self):
        response = self.client.delete(
            "http://127.0.0.1:8000/api/cinema/actors/1/",
        )
        db_actors_id_1 = Actor.objects.filter(id=1)
        self.assertEqual(db_actors_id_1.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminActorApiTests(TestCase):
    def setUp(self):
        Actor.objects.create(first_name="George", last_name="Clooney")
        Actor.objects.create(first_name="Keanu", last_name="Reeves")

        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_actors(self):
        response = self.client.get("/api/cinema/actors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actors_full_names = [actor["full_name"] for actor in response.data]
        self.assertEqual(sorted(actors_full_names), ["George Clooney", "Keanu Reeves"])

    def test_post_actors(self):
        response = self.client.post(
            "/api/cinema/actors/",
            {
                "first_name": "Scarlett",
                "last_name": "Johansson",
            },
        )
        db_actors = Actor.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_actors.count(), 3)
        self.assertEqual(db_actors.filter(first_name="Scarlett").count(), 1)

    def test_get_invalid_actor(self):
        response = self.client.get("/api/cinema/actors/1001/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_actor(self):
        response = self.client.put(
            "/api/cinema/actors/1/",
            {
                "first_name": "Scarlett",
                "last_name": "Johansson",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_actor(self):
        response = self.client.delete(
            "http://127.0.0.1:8000/api/cinema/actors/1/",
        )
        db_actors_id_1 = Actor.objects.filter(id=1)
        self.assertEqual(db_actors_id_1.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
