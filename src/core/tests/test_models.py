import datetime
from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model

from core import models


# helper for logins
def sample_user(email='test@example.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'nick@holmegrown.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@HOLMEGROWN.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@Holmegrown.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Bessie'
        )

        self.assertEqual(str(tag), tag.name)

    def test_cow_str(self):
        """Test creating a bovid"""
        cow = models.Bovid.objects.create(
            type_of_bovid='Brahman',
            user=sample_user(),
            name='Bessie'
        )

        self.assertEqual(str(cow), cow.name)
        self.assertEqual('Brahman', cow.type_of_bovid)

    def test_life_events(self):
        """Test that a life event can be created"""
        user = sample_user()
        cow = models.Bovid.objects.create(
            type_of_bovid='Brahman',
            user=user,
            name='Bessie'
        )
        event = models.LifeEvent.objects.create(
            event_type='Innoculation',
            event_date=datetime.date.today(),
            notes='Some test text to seeeee',
            user=user,
            bovid=cow
        )
        self.assertEqual(str(event), event.event_type)

    @patch('uuid.uuid4')
    def test_bovid_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.bovid_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/bovid/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
