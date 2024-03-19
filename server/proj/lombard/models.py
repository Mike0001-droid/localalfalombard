from django.db import models
from account.models import Profile
from django.template.defaultfilters import slugify  # new


# Create your models here.
class Favorites(models.Model):
    user = models.ForeignKey(Profile, verbose_name='Пользователь', related_name='favorites', on_delete=models.CASCADE)
    ticket = models.CharField('УИД билета', max_length=63)

    class Meta:
        verbose_name = 'Избранный билет'
        verbose_name_plural = "Избранные билеты"

    def __str__(self):
        return f"{self.user} {self.ticket}"


class Page(models.Model):
    title = models.CharField('Заголовок', max_length=255, null=True, blank=True)
    body = models.TextField('Текст')
    slug = models.SlugField('Ссылка', unique=True, null=False)
    date_updated = models.DateTimeField('ДатаВремя обновления', auto_now=True)
    date_publication = models.DateTimeField('ДатаВремя публикации', auto_now_add=True)
    publication = models.BooleanField('Публиковать?', default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
