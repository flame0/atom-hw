from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .utils import UserManager


class User(AbstractBaseUser):
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Номер телефона', max_length=15)
    last_name = models.CharField('Фамилия', max_length=50)
    first_name = models.CharField('Имя', max_length=50)
    age = models.PositiveIntegerField('Возраст', null=True, blank=True)
    region = models.CharField('Регион', max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'last_name', 'first_name']

    objects = UserManager()

    def get_full_name(self):
        return "%s (%s %s)".format(self.email, self.last_name, self.first_name)

    def get_short_name(self):
        return "%s".format(self.email)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
