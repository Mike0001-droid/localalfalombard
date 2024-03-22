from conf.celery import app
from django.core.mail import EmailMultiAlternatives

from account.models import Profile
from lombard.service import LombardService
from conf import settings
import logging
from settings_site.config_models import SiteConfiguration
logger = logging.getLogger('notify')


@app.task
def notify_clients():
    logger.info(f'Начата задача по оповещению пользователей')

    try:
        service = LombardService()
        tickets = service.get_tickets_ending()
        for ticket in tickets:
            client_id = ticket.get('clientId', None)
            try:
                profile = Profile.objects.get(client_id=client_id, notify=True)
                day_ending: int = int(ticket.get('dayEnding'))
                days = f'{day_ending} дней' if day_ending > 5 else f'{day_ending} дня'
                message = f"""<pre>
Уважаемый Залогодатель! По Вашему залоговому билету №{ticket.get('ticket')} до окончания льготного срока осталось {days}.
Просим Вас до истечения указанного срока погасить образовавшуюся по данному залоговому билету задолженность.
Сделать это возможно или через <a href="{settings.CLIENT_URL}">Ваш Личный кабинет</a> или непосредственно в подразделении ломбарда, в котором был выдан займ.
Сумму задолженности Вы всегда можете уточнить в Вашем Личном кабинете.

Спасибо!

С уважением,
администрация ломбарда.
                """
                mail = EmailMultiAlternatives(
                    subject='Уведомление о скором окончании льготного периода в ломбарде',
                    body=message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[profile.email],
                )
                mail.attach_alternative(message, "text/html")
                mail.send()
            except Profile.DoesNotExist:
                continue
            except Exception as e:
                logger.error(f'Пользователь с {client_id}, ошибка: {str(e)}')
                continue
    except Exception as e:
        logger.error(f'Задача прошла не успешно, причина: {str(e)}\n')


