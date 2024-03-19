from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, *args, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Емайл', max_length=255, unique=True,)
    client_id = models.CharField('Идентификатор пользователя в 1С', max_length=255, blank=True, unique=True)
    fio = models.CharField('ФИО', max_length=150, blank=True, null=True, default='')
    #series = models.CharField('Серия паспорта', max_length=150)
    #number = models.CharField('Номер паспорта', max_length=150)
    phone = models.CharField('Телефон', max_length=15)
    notify = models.BooleanField('Оповещения', default=True)
    is_active = models.BooleanField('Активный', help_text='Отметьте, если пользователь активен.', default=True)
    is_staff = models.BooleanField('Статус персонала', help_text='Отметьте, если пользователь может входить в '
                                                                 'административную часть сайта.', default=False)

    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.email}'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class FormMessage(models.Model):
    person = models.CharField('Имя', max_length=255)
    email = models.EmailField('Email', max_length=255)
    phone = models.CharField('Телефон', max_length=255)
    question = models.TextField('Текст сообщения')
    date_publication = models.DateTimeField('ДатаВремя публикации', auto_now_add=True)
    publication = models.BooleanField('Публиковать?', default=True)

    def __str__(self):
        return f'{self.email} - {self.person}'

    class Meta:
        verbose_name = 'Вопрос пользователя'
        verbose_name_plural = 'Вопросы ользователей'


class SiteInfo(models.Model):
    config_name = models.CharField("Название конфигурации", max_length=100)
    phone = models.CharField('Телефон', max_length=100, blank=True, null=True)
    email = models.EmailField('Email', max_length=100, blank=True, null=True)
    footer_text = models.TextField('Текст футера')

    class Meta:
        verbose_name = 'Информация сайта'
        verbose_name_plural = 'Информация по сайту'

    def __str__(self) -> str:
        return self.config_name
