from django.db import models
from tinymce.models import HTMLField
from settings_site.single_configuration import SingletonModel
from datetime import datetime 

class SiteConfiguration(SingletonModel):
    text_error = HTMLField('Текст ошибки')
    block_time = models.IntegerField('Время блокировки доступа в 1с (в минутах)', default=0)
    access_flag = models.BooleanField('Доступ в 1с', default=False)
    update_date = models.DateTimeField('Время последнего обновления', auto_now=True)
    end_block_date = models.DateTimeField('Время конца блокировки', default=datetime.now())

    def __str__(self):
        return u"Настройки доступа к 1с"

    class Meta:
        verbose_name = "Настройки доступа к 1с"
        verbose_name_plural = "Настройки доступа к 1с"
