'''
User & Profile models.
'''

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    '''User manager.'''
    def create_user(self, username, password=None, **extra_fields):
        '''Method that creates and returns a new user.'''
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        '''Method that creates and returns a new superuser.'''
        user = self.model(username=username)
        user.is_staff = True
        user.is_superuser=True
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''User model.'''
    username = models.CharField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Profile(models.Model):
    '''Profile model.'''
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    '''Creates a profile for a new user instance right after the user is saved.'''
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()
    
    return user_profile

'''Signal for create_profile'''
post_save.connect(create_profile, sender=User)