from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

# Create your tests here.


class TestModel(TestCase):
    """
    Class to test System.models
    """

    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
            email='test@test.in',
            full_name='test',
            phone_number='1234567890',
            is_verified=True,
        )
        self.client.login(username='test', password='test')

    def test_user_model(self):
        """
        Test User model
        """
        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.email, 'test@test.in')
