from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from settings_site.config_models import SiteConfiguration
from datetime import datetime, timedelta
from settings_site.tasks import access_block

@receiver (pre_save, sender=SiteConfiguration)
def pre_save_obj(sender, instance, **kwargs):
    obj = SiteConfiguration.objects.get()
    if instance.access_flag == False and instance.block_time > 0:
        instance.end_block_date = instance.update_date + timedelta(minutes=instance.block_time)
        #access_block.apply_async(eta=datetime.now() + timedelta(minutes=instance.block_time))
    