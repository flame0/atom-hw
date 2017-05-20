from django.db import models
from django.core.mail import send_mail
from django.utils import six, timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,AbstractUser
from .utils import UserManager

# http://techqa.info/programming/question/18769729/django---removing-username-from-user-model
# поч так а не иначе


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Номер телефона', max_length=15)
    last_name = models.CharField('Фамилия', max_length=50)
    first_name = models.CharField('Имя', max_length=50)
    age = models.PositiveIntegerField('Возраст', null=True, blank=True)
    region = models.CharField('Регион', max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'last_name', 'first_name']

    objects = UserManager()

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

