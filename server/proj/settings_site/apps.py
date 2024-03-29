from django.apps import AppConfig


class SettingsSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings_site'
    verbose_name = 'Настройки сайта'

    def ready(self):
        import settings_site.signals