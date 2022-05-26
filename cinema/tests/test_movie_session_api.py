import datetime

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from cinema.models import Movie, Genre, Actor, MovieSession, CinemaHall
from user.tests.test_user_api import create_user


class PublicMovieSessionApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get("http://127.0.0.1:8000/api/cinema/movie_sessions/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMovieSessionApiTests(TestCase):
    def setUp(self):
        drama = Genre.objects.create(
            name="Drama",
        )
        comedy = Genre.objects.create(
            name="Comedy",
        )
        actress = Actor.objects.create(first_name="Kate", last_name="Winslet")
        self.movie = Movie.objects.create(
            title="Titanic",
            description="Titanic description",
            duration=123,
        )
        self.movie.genres.add(drama)
        self.movie.genres.add(comedy)
        self.movie.actors.add(actress)
        self.cinema_hall = CinemaHall.objects.create(
            name="White",
            rows=10,
            seats_in_row=14,
        )
        self.movie_session = MovieSession.objects.create(
            movie=self.movie,
            cinema_hall=self.cinema_hall,
            show_time=datetime.datetime(
                year=2022,
                month=9,
                day=2,
            ),
        )

        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_movie_sessions(self):
        movie_sessions = self.client.get("/api/cinema/movie_sessions/")
        movie_session = {
            "movie_title": "Titanic",
            "cinema_hall_name": "White",
            "cinema_hall_capacity": 140,
        }
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        for field in movie_session:
            self.assertEqual(movie_sessions.data[0][field], movie_session[field])

    def test_get_movie_sessions_filtered_by_date(self):
        movie_sessions = self.client.get("/api/cinema/movie_sessions/?date=2022-09-02")
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 1)

        movie_sessions = self.client.get("/api/cinema/movie_sessions/?date=2022-09-01")
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

    def test_get_movie_sessions_filtered_by_movie(self):
        movie_sessions = self.client.get(
            f"/api/cinema/movie_sessions/?movie={self.movie.id}"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 1)

        movie_sessions = self.client.get("/api/cinema/movie_sessions/?movie=1234")
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

    def test_get_movie_sessions_filtered_by_movie_and_data(self):
        movie_sessions = self.client.get(
            f"/api/cinema/movie_sessions/?movie={self.movie.id}&date=2022-09-2"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 1)

        movie_sessions = self.client.get(
            "/api/cinema/movie_sessions/?movie=1234&date=2022-09-2"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

        movie_sessions = self.client.get(
            f"/api/cinema/movie_sessions/?movie={self.movie.id}&date=2022-09-3"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

    def test_post_movie_session(self):
        movies = self.client.post(
            "/api/cinema/movie_sessions/",
            {"movie": 1, "cinema_hall": 1, "show_time": datetime.datetime.now()},
        )
        movie_sessions = MovieSession.objects.all()
        self.assertEqual(movies.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(movie_sessions.count(), 1)

    def test_get_movie_session(self):
        response = self.client.get("/api/cinema/movie_sessions/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["movie"]["title"], "Titanic")
        self.assertEqual(response.data["movie"]["description"], "Titanic description")
        self.assertEqual(response.data["movie"]["duration"], 123)
        self.assertEqual(response.data["movie"]["genres"], ["Drama", "Comedy"])
        self.assertEqual(response.data["movie"]["actors"], ["Kate Winslet"])
        self.assertEqual(response.data["cinema_hall"]["capacity"], 140)
        self.assertEqual(response.data["cinema_hall"]["rows"], 10)
        self.assertEqual(response.data["cinema_hall"]["seats_in_row"], 14)
        self.assertEqual(response.data["cinema_hall"]["name"], "White")

    def test_put_movie_session(self):
        response = self.client.put(
            "/api/cinema/movie_sessions/1/",
            {"movie": 1, "cinema_hall": 1, "show_time": datetime.datetime.now()},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_movie_session(self):
        response = self.client.delete("/api/cinema/movie_sessions/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieSessionApiTests(TestCase):
    def setUp(self):
        drama = Genre.objects.create(
            name="Drama",
        )
        comedy = Genre.objects.create(
            name="Comedy",
        )
        actress = Actor.objects.create(first_name="Kate", last_name="Winslet")
        self.movie = Movie.objects.create(
            title="Titanic",
            description="Titanic description",
            duration=123,
        )
        self.movie.genres.add(drama)
        self.movie.genres.add(comedy)
        self.movie.actors.add(actress)
        self.cinema_hall = CinemaHall.objects.create(
            name="White",
            rows=10,
            seats_in_row=14,
        )
        self.movie_session = MovieSession.objects.create(
            movie=self.movie,
            cinema_hall=self.cinema_hall,
            show_time=datetime.datetime(
                year=2022,
                month=9,
                day=2,
            ),
        )

        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_movie_sessions(self):
        movie_sessions = self.client.get("/api/cinema/movie_sessions/")
        movie_session = {
            "movie_title": "Titanic",
            "cinema_hall_name": "White",
            "cinema_hall_capacity": 140,
        }
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        for field in movie_session:
            self.assertEqual(movie_sessions.data[0][field], movie_session[field])

    def test_get_movie_sessions_filtered_by_date(self):
        movie_sessions = self.client.get("/api/cinema/movie_sessions/?date=2022-09-02")
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 1)

        movie_sessions = self.client.get("/api/cinema/movie_sessions/?date=2022-09-01")
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

    def test_get_movie_sessions_filtered_by_movie(self):
        movie_sessions = self.client.get(
            f"/api/cinema/movie_sessions/?movie={self.movie.id}"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 1)

        movie_sessions = self.client.get("/api/cinema/movie_sessions/?movie=1234")
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

    def test_get_movie_sessions_filtered_by_movie_and_data(self):
        movie_sessions = self.client.get(
            f"/api/cinema/movie_sessions/?movie={self.movie.id}&date=2022-09-2"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 1)

        movie_sessions = self.client.get(
            "/api/cinema/movie_sessions/?movie=1234&date=2022-09-2"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

        movie_sessions = self.client.get(
            f"/api/cinema/movie_sessions/?movie={self.movie.id}&date=2022-09-3"
        )
        self.assertEqual(movie_sessions.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_sessions.data), 0)

    def test_post_movie_session(self):
        movies = self.client.post(
            "/api/cinema/movie_sessions/",
            {"movie": 1, "cinema_hall": 1, "show_time": datetime.datetime.now()},
        )
        movie_sessions = MovieSession.objects.all()
        self.assertEqual(movies.status_code, status.HTTP_201_CREATED)
        self.assertEqual(movie_sessions.count(), 2)

    def test_get_movie_session(self):
        response = self.client.get("/api/cinema/movie_sessions/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["movie"]["title"], "Titanic")
        self.assertEqual(response.data["movie"]["description"], "Titanic description")
        self.assertEqual(response.data["movie"]["duration"], 123)
        self.assertEqual(response.data["movie"]["genres"], ["Drama", "Comedy"])
        self.assertEqual(response.data["movie"]["actors"], ["Kate Winslet"])
        self.assertEqual(response.data["cinema_hall"]["capacity"], 140)
        self.assertEqual(response.data["cinema_hall"]["rows"], 10)
        self.assertEqual(response.data["cinema_hall"]["seats_in_row"], 14)
        self.assertEqual(response.data["cinema_hall"]["name"], "White")

    def test_put_movie_session(self):
        response = self.client.put(
            "/api/cinema/movie_sessions/1/",
            {"movie": 1, "cinema_hall": 1, "show_time": datetime.datetime.now()},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_movie_session(self):
        response = self.client.delete("/api/cinema/movie_sessions/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
