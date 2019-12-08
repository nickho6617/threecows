from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Bovid, Tag, LifeEvent

from cattle.serializers import BovidSerializer, BovidDetailSerializer

CATTLE_URL = reverse('cattle:bovid-list')


# Helper functions to setup data
def sample_tag(user, name='inspuitings klaar'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def detail_url(bovid_id):
    """Return bovid detail URL"""
    return reverse('cattle:bovid-detail', args=[bovid_id])


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


def sample_event(user, **params):
    """Create and return a sample life event"""
    return LifeEvent.objects.create(
        event_type='Inspuitings',
        event_date='2019-11-30',
        notes='this is a test note'
        )


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

    def test_view_bovid_detail(self):
        """Test viewing detail of a bovid"""

        cow = sample_bovine(user=self.user)
        cow.tags.add(sample_tag(user=self.user))
        # cow.events.add(sample_event(user=self.user))

        url = detail_url(cow.id)
        res = self.client.get(url)

        serializer = BovidDetailSerializer(cow)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_cow(self):
        """Test creating cow"""
        user = self.user.id
        payload = {
                'type_of_bovid': 'koei',
                'name': 'kleintjie',
                'user': user
            }
        res = self.client.post(CATTLE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_cow_with_tags(self):
        """Test creating a cow with tags"""
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
            'tags': [tag1.id, tag2.id],
            'type_of_bovid': 'koei',
            'name': 'kleintjie',
            'price': 5.00,
            'user': self.user.id
        }
        res = self.client.post(CATTLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        cow = Bovid.objects.get(id=res.data['id'])
        tags = cow.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)
