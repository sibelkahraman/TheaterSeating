from django.test import TestCase
from rest_framework.test import APIClient

from seat.create_seat import CreateSeat
from seat.models import Seat


class TestCreateSeatAPI(TestCase):
    def setUp(self) -> None:
        self.api = APIClient()

    def create_db(self):
        self.api.get('/create')

    def test_create_endpoint_when_db_is_empty(self):
        response = self.api.get('/create')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, 'Database is created')

    def test_create_endpoint_when_db_is_not_empty(self):
        self.create_db()
        response = self.api.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Database is already created')


class TestCreateSeat(TestCase):
    def setUp(self) -> None:
        self.seat = CreateSeat()

    def test_create_seat(self):
        response = self.seat.seat()
        seat = Seat.objects.first()
        # test only 1 and 2 ranks are main hall

        self.assertEqual(Seat.objects.filter(section=1).count(), 160)

        self.assertIsNotNone(Seat.objects.filter(section=1, rank=1))
        self.assertEqual(Seat.objects.filter(section=1, rank=1).count(), 40)

        self.assertIsNotNone(Seat.objects.filter(section=1, rank=2))
        self.assertEqual(Seat.objects.filter(section=1, rank=2).count(), 120)

        self.assertEqual(Seat.objects.filter(section=1, rank=3).count(), 0)

        # test second hall

        self.assertEqual(Seat.objects.filter(section=2).count(), 160)

        self.assertIsNotNone(Seat.objects.filter(section=1, rank=1))
        self.assertEqual(Seat.objects.filter(section=2, rank=1).count(), 20)

        self.assertIsNotNone(Seat.objects.filter(section=1, rank=2))
        self.assertEqual(Seat.objects.filter(section=2, rank=2).count(), 40)

        self.assertIsNotNone(Seat.objects.filter(section=1, rank=3))
        self.assertEqual(Seat.objects.filter(section=2, rank=3).count(), 100)

        # test third hall

        self.assertEqual(Seat.objects.filter(section=3).count(), 160)

        self.assertEqual(Seat.objects.filter(section=3, rank=1).count(), 0)

        self.assertIsNotNone(Seat.objects.filter(section=3, rank=2))
        self.assertEqual(Seat.objects.filter(section=3, rank=2).count(), 60)

        self.assertIsNotNone(Seat.objects.filter(section=1, rank=3))
        self.assertEqual(Seat.objects.filter(section=3, rank=3).count(), 100)

        self.assertIsNotNone(seat)
        print(response)
