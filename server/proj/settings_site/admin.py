from django.contrib import admin
from settings_site.admin_configuration import SingletonModelAdmin
from settings_site.config_models import SiteConfiguration


admin.site.register(SiteConfiguration, SingletonModelAdmin)

