from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone, last_name, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have an phone number')
        if not last_name:
            raise ValueError('Users must have an last name')
        if not first_name:
            raise ValueError('Users must have an first name')
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            last_name=last_name,
            first_name=first_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, last_name, first_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            phone=phone,
            last_name=last_name,
            first_name=first_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

