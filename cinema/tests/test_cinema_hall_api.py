from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from cinema.models import CinemaHall
from user.tests.test_user_api import create_user


class PublicCinemaHallApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get("http://127.0.0.1:8000/api/cinema/cinema_halls/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCinemaHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        CinemaHall.objects.create(
            name="Blue",
            rows=15,
            seats_in_row=20,
        )
        CinemaHall.objects.create(
            name="VIP",
            rows=6,
            seats_in_row=8,
        )
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_cinema_halls(self):
        response = self.client.get("/api/cinema/cinema_halls/")
        blue_hall = {
            "name": "Blue",
            "rows": 15,
            "seats_in_row": 20,
            "capacity": 300,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], blue_hall["name"])
        self.assertEqual(response.data[0]["rows"], blue_hall["rows"])
        self.assertEqual(response.data[0]["seats_in_row"], blue_hall["seats_in_row"])
        vip_hall = {
            "name": "VIP",
            "rows": 6,
            "seats_in_row": 8,
            "capacity": 48,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[1]["name"], vip_hall["name"])
        self.assertEqual(response.data[1]["rows"], vip_hall["rows"])
        self.assertEqual(response.data[1]["seats_in_row"], vip_hall["seats_in_row"])

    def test_post_cinema_halls(self):
        response = self.client.post(
            "/api/cinema/cinema_halls/",
            {
                "name": "Yellow",
                "rows": 14,
                "seats_in_row": 15,
            },
        )
        db_cinema_halls = CinemaHall.objects.all()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(db_cinema_halls.count(), 2)
        self.assertEqual(db_cinema_halls.filter(name="Yellow").count(), 0)

    def test_get_cinema_hall(self):
        response = self.client.get("/api/cinema/cinema_halls/2/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_cinema_hall(self):
        response = self.client.get("/api/cinema/cinema_halls/1001/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_cinema_hall(self):
        response = self.client.put(
            "/api/cinema/cinema_halls/1/",
            {
                "name": "Yellow",
                "rows": 14,
                "seats_in_row": 15,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_cinema_hall(self):
        response = self.client.patch(
            "/api/cinema/cinema_halls/1/",
            {
                "name": "Green",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(CinemaHall.objects.get(id=1).name, "Blue")

    def test_delete_cinema_hall(self):
        response = self.client.delete(
            "/api/cinema/cinema_halls/1/",
        )
        db_cinema_halls_id_1 = CinemaHall.objects.filter(id=1)
        self.assertEqual(db_cinema_halls_id_1.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminCinemaHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        CinemaHall.objects.create(
            name="Blue",
            rows=15,
            seats_in_row=20,
        )
        CinemaHall.objects.create(
            name="VIP",
            rows=6,
            seats_in_row=8,
        )
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_cinema_halls(self):
        response = self.client.get("/api/cinema/cinema_halls/")
        blue_hall = {
            "name": "Blue",
            "rows": 15,
            "seats_in_row": 20,
            "capacity": 300,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], blue_hall["name"])
        self.assertEqual(response.data[0]["rows"], blue_hall["rows"])
        self.assertEqual(response.data[0]["seats_in_row"], blue_hall["seats_in_row"])
        vip_hall = {
            "name": "VIP",
            "rows": 6,
            "seats_in_row": 8,
            "capacity": 48,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[1]["name"], vip_hall["name"])
        self.assertEqual(response.data[1]["rows"], vip_hall["rows"])
        self.assertEqual(response.data[1]["seats_in_row"], vip_hall["seats_in_row"])

    def test_post_cinema_halls(self):
        response = self.client.post(
            "/api/cinema/cinema_halls/",
            {
                "name": "Yellow",
                "rows": 14,
                "seats_in_row": 15,
            },
        )
        db_cinema_halls = CinemaHall.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_cinema_halls.count(), 3)
        self.assertEqual(db_cinema_halls.filter(name="Yellow").count(), 1)

    def test_get_cinema_hall(self):
        response = self.client.get("/api/cinema/cinema_halls/2/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_cinema_hall(self):
        response = self.client.get("/api/cinema/cinema_halls/1001/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_cinema_hall(self):
        response = self.client.put(
            "/api/cinema/cinema_halls/1/",
            {
                "name": "Yellow",
                "rows": 14,
                "seats_in_row": 15,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_cinema_hall(self):
        response = self.client.patch(
            "/api/cinema/cinema_halls/1/",
            {
                "name": "Green",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(CinemaHall.objects.get(id=1).name, "Blue")

    def test_delete_cinema_hall(self):
        response = self.client.delete(
            "/api/cinema/cinema_halls/1/",
        )
        db_cinema_halls_id_1 = CinemaHall.objects.filter(id=1)
        self.assertEqual(db_cinema_halls_id_1.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
