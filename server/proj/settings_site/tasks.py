from conf.celery import app
import logging
from settings_site.config_models import SiteConfiguration
logger = logging.getLogger('notify')

@app.task
def access_block():
    logger.info(f'Начата задача по ограничению доступа в 1с')
    try:
        instance = SiteConfiguration.objects.all()
        for i in instance:
            if i.block_time != 0 and i.access_flag == False:
                i.block_time = 0
                i.access_flag = True
                
    except Exception as e:
        logger.error(f'Задача прошла не успешно, причина: {str(e)}\n')