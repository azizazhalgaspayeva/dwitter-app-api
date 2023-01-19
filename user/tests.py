'''
Test user app functionality.
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from . import models


def create_user(username, password, **extra_fields):
    '''Creates and returns a new user object.'''
    return get_user_model().objects.create_user(username, password, **extra_fields)


class UserModelTests(TestCase):
    '''Test user model.'''
    def test_create_user_successful(self):
        '''Test creating a new user is successful.'''
        username = 'testuser'
        password = 'testpassword'
        user = create_user(username, password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_username_fails(self):
        '''Test creating a user without username raises error.'''
        with self.assertRaises(ValueError):
            create_user('', 'testpassword')

    def test_create_superuser(self):
        '''Test creating a new user is successful.'''
        username = 'testuser'
        password = 'testpassword'
        user = get_user_model().objects.create_superuser(username, password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_profile_along_with_user(self):
        '''Test a new profile is automatically assigned to a new user.'''
        username = 'testuser'
        password = 'testpassword'
        user = create_user(username, password)
        profile = models.Profile.objects.filter(user=user)
        
        self.assertTrue(profile.exists())


class ProfileModelTests(TestCase):
    '''Test profile model.'''
    def test_create_profile_successful(self):
        '''Test creating a new profile is successful.'''
        username = 'testuser'
        password = 'testpassword'
        user = create_user(username, password)

        profile = models.Profile.objects.filter(user=user)[0]

        self.assertEqual(profile.user.username, username)
        self.assertTrue(profile.user.check_password(password))