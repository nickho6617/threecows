from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Bovid, LifeEvent

from cattle.serializers import LifeEventSerializer


LIFEEVENT_URL = reverse('cattle:lifeevent-list')


class PublicEventsApiTests(TestCase):
    """Test the publically available life events API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(LIFEEVENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEventsAPITests(TestCase):
    """Test life events can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@holmegrownsoftware.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_life_event_list(self):
        """Test retrieving a list of life events"""
        a_cow = Bovid.objects.create(
            name='Big',
            type_of_bovid='Brahman',
            user=self.user
        )
        LifeEvent.objects.create(
            bovid=a_cow,
            event_type='birth',
            event_date='2019-12-01'
            )
        LifeEvent.objects.create(
            bovid=a_cow,
            event_type='suckled',
            event_date='2019-12-01'
            )

        res = self.client.get(LIFEEVENT_URL)

        life_events = LifeEvent.objects.all().order_by('id')
        serializer = LifeEventSerializer(life_events, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializer.data[0])
        self.assertEqual(res.data[1], serializer.data[1])
