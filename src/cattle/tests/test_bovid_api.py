from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Bovid

from cattle.serializers import BovidSerializer


CATTLE_URL = reverse('cattle:bovid-list')


def sample_bovine(user, **params):
    """Create and return a sample animal"""
    defaults = {
        'mothers_name': 'bokkie',
        'fathers_name': 'boelie',
        'type_of_bovid': 'koei',
        'name': 'kleintjie',
        'price': 5.00,
    }
    defaults.update(params)

    return Bovid.objects.create(user=user, **defaults)


class PublicBovidApiTests(TestCase):
    """Test unauthenticated bovid API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authentication is required"""
        res = self.client.get(CATTLE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBovidApiTests(TestCase):
    """Test authenticated bovid API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@holmegrownsoftware.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_bovid(self):
        """Test retrieving list of cows"""
        sample_bovine(user=self.user)
        sample_bovine(user=self.user)

        res = self.client.get(CATTLE_URL)

        cows = Bovid.objects.all().order_by('-id')
        serializer = BovidSerializer(cows, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_bovines_limited_to_user(self):
        """Test retrieving bovines for user"""
        user2 = get_user_model().objects.create_user(
            'other@holmegrownsoftware.com',
            'pass'
        )
        sample_bovine(user=user2)
        sample_bovine(user=self.user)

        res = self.client.get(CATTLE_URL)

        cattle = Bovid.objects.filter(user=self.user)
        serializer = BovidSerializer(cattle, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
