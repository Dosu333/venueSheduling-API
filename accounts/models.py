from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None ,**extra_fields):
        """Createes and saves new user"""

        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self,email, password):
        """Creates and saves superuser"""
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser =True
        user.save()

        return user

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, on_delete = models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # roles = models.ManyToManyField(Group, blank=True, related_name='role')

    objects = UserManager()

    USERNAME_FIELD = 'email'