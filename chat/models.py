from email.policy import default
from enum import unique
from tabnanny import verbose
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self,pseudo, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError(_('The Email must be set'))
        if not pseudo:
            raise ValueError(_('The Pseudo must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,pseudo=pseudo, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, pseudo, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(pseudo,email,password,**extra_fields)

class User(AbstractUser):

    pseudo = models.CharField(max_length=50,unique=True)
    image = models.ImageField(upload_to='user_profil/', max_length=500, default='')
    email = models.EmailField(max_length=50,unique=True)
    online = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta :
        verbose_name = 'Utilisateur'
    
    def __str__(self) -> str:
        return self.pseudo


class Message (models.Model):

    creator_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    creation_date = models.DateTimeField(default=timezone.now)
