from datetime import datetime

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from cinema.models import Movie, Genre, Actor, CinemaHall, MovieSession, Ticket, Order
from user.tests.test_user_api import create_user


class PublicOrderApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get("http://127.0.0.1:8000/api/cinema/orders/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTests(TestCase):
    def setUp(self):
        self.drama = Genre.objects.create(
            name="Drama",
        )
        self.comedy = Genre.objects.create(
            name="Comedy",
        )
        self.actress = Actor.objects.create(first_name="Kate", last_name="Winslet")
        self.movie = Movie.objects.create(
            title="Titanic",
            description="Titanic description",
            duration=123,
        )
        self.movie.genres.add(self.drama)
        self.movie.genres.add(self.comedy)
        self.movie.actors.add(self.actress)
        self.cinema_hall = CinemaHall.objects.create(
            name="White",
            rows=10,
            seats_in_row=14,
        )
        self.movie_session = MovieSession.objects.create(
            movie=self.movie, cinema_hall=self.cinema_hall, show_time=datetime.now()
        )
        self.another_user = create_user(
            username="user",
            email="user@test.com",
            password="userpass",
        )
        self.order = Order.objects.create(user=self.another_user)
        self.ticket = Ticket.objects.create(
            movie_session=self.movie_session, row=2, seat=12, order=self.order
        )

        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_order(self):
        orders_response = self.client.get("/api/cinema/orders/")
        self.assertEqual(orders_response.status_code, status.HTTP_200_OK)
        self.assertEqual(orders_response.data["count"], 0)

    def test_create_order(self):
        orders_response = self.client.post("/api/cinema/orders/", {})

        self.assertEqual(orders_response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminOrderApiTests(TestCase):
    def setUp(self):
        self.drama = Genre.objects.create(
            name="Drama",
        )
        self.comedy = Genre.objects.create(
            name="Comedy",
        )
        self.actress = Actor.objects.create(first_name="Kate", last_name="Winslet")
        self.movie = Movie.objects.create(
            title="Titanic",
            description="Titanic description",
            duration=123,
        )
        self.movie.genres.add(self.drama)
        self.movie.genres.add(self.comedy)
        self.movie.actors.add(self.actress)
        self.cinema_hall = CinemaHall.objects.create(
            name="White",
            rows=10,
            seats_in_row=14,
        )
        self.movie_session = MovieSession.objects.create(
            movie=self.movie, cinema_hall=self.cinema_hall, show_time=datetime.now()
        )
        self.another_user = create_user(
            username="user",
            email="user@test.com",
            password="userpass",
        )
        self.order = Order.objects.create(user=self.another_user)
        self.ticket = Ticket.objects.create(
            movie_session=self.movie_session, row=2, seat=12, order=self.order
        )

        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_order(self):
        orders_response = self.client.get("/api/cinema/orders/")
        self.assertEqual(orders_response.status_code, status.HTTP_200_OK)
        self.assertEqual(orders_response.data["count"], 0)

    def test_create_order(self):
        orders_response = self.client.post("/api/cinema/orders/", {})

        self.assertEqual(orders_response.status_code, status.HTTP_400_BAD_REQUEST)
