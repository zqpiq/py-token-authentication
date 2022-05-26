from django.test import TestCase

from cinema.views import (
    GenreViewSet,
    ActorViewSet,
    CinemaHallViewSet,
    MovieViewSet,
    OrderViewSet,
)


class ApiViewTests(TestCase):
    def test_extends_mixins(self):
        self.assertEqual(
            str(GenreViewSet.__bases__),
            "(<class 'rest_framework.mixins.ListModelMixin'>,"
            " <class 'rest_framework.mixins.CreateModelMixin'>,"
            " <class 'rest_framework.viewsets.GenericViewSet'>)",
        )
        self.assertEqual(
            str(ActorViewSet.__bases__),
            "(<class 'rest_framework.mixins.ListModelMixin'>,"
            " <class 'rest_framework.mixins.CreateModelMixin'>,"
            " <class 'rest_framework.viewsets.GenericViewSet'>)",
        )
        self.assertEqual(
            str(CinemaHallViewSet.__bases__),
            "(<class 'rest_framework.mixins.ListModelMixin'>,"
            " <class 'rest_framework.mixins.CreateModelMixin'>,"
            " <class 'rest_framework.viewsets.GenericViewSet'>)",
        )
        self.assertEqual(
            str(MovieViewSet.__bases__),
            "(<class 'rest_framework.mixins.ListModelMixin'>,"
            " <class 'rest_framework.mixins.CreateModelMixin'>,"
            " <class 'rest_framework.mixins.RetrieveModelMixin'>,"
            " <class 'rest_framework.viewsets.GenericViewSet'>)",
        )
        self.assertEqual(
            str(OrderViewSet.__bases__),
            "(<class 'rest_framework.mixins.ListModelMixin'>,"
            " <class 'rest_framework.mixins.CreateModelMixin'>,"
            " <class 'rest_framework.mixins.RetrieveModelMixin'>,"
            " <class 'rest_framework.viewsets.GenericViewSet'>)",
        )
