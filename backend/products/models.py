from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class Product(models.Model):
    title=models.CharField(max_length= 200)
    images=models.CharField(max_length= 200)
    likes=models.PositiveIntegerField(default=0)


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):

        if not username:
            raise ValueError('Users must have an username')

        user = self.model(username =username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username):

        user = self.create_user(
            username = username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    firstname = models.CharField(max_length=200,default=None)
    lastname = models.CharField(max_length=200,default=None)
    email = models.EmailField( max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

