from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=16, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag for a user to add to livestock"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Bovid(models.Model):
    """This model will hold the cows in their various shapes and form"""

    # image = models.ImageField(upload_to='images/', blank=True)
    mothers_name = models.CharField(max_length=150, blank=True)
    fathers_name = models.CharField(max_length=150, blank=True)
    type_of_bovid = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=255)
    breeder = models.CharField(max_length=250, blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
        )
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    date_sold = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class LifeEvent(models.Model):
    """Model to hold any events related to an animal.
    eg vet, grazing, giving birth
    """
    bovid = models.ForeignKey(
        Bovid,
        on_delete=models.CASCADE,
        related_name='bovids'
        )
    event_type = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    event_date = models.DateField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.event_type
