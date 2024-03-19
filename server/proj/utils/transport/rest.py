import pytz
import requests

from typing import Optional
from datetime import datetime

from django.conf import settings
from requests import HTTPError

from payments.models import TerminalsPaymo
from utils.transport import Transport, TransportError

import logging
logger = logging.getLogger('transport')


if settings.DEBUG:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


URL = settings.TRANSPORT_1C['URL']
USERNAME = settings.TRANSPORT_1C['USERNAME']
PASSWORD = settings.TRANSPORT_1C['PASSWORD']
TIMEOUT = settings.TRANSPORT_1C['TIMEOUT']


class RESTError(TransportError):
    pass


class REST(Transport):
    url = URL
    username = USERNAME
    password = PASSWORD
    timeout = TIMEOUT

    def call(self, method, *args, **kwargs):
        logger.info('Calling REST method %s with args: %s' % (method, kwargs))
        # print('Calling REST method %s with args: %s' % (method, kwargs))

        assert not (args and kwargs), 'args and kwargs cannot be passed together'

        if args:
            data = {"params": args[0]}
        else:
            data = {"params": kwargs}
        try:
            response = self._request(method, data)
        except Exception as e:
            logger.debug(e)
            return e

        if response.status_code == 404:
            raise NotImplementedError('REST method %s does not exist' % method)
        try:
            text_error = response.text
        except AttributeError:
            text_error = None

        try:
            response.raise_for_status()
        except HTTPError as e:
            logger.exception('Failed response TEXT: %s' % text_error)
            logger.exception('Failed error: %s' % str(e))
            raise e

        result = response.json()
        logger.debug('Result: %s \n' % result)

        if result.get('result') is None:
            raise RESTError(result)

        return result

    def _request(self, method, data):
        response = requests.post(
            self.url + method,
            json=data,
            auth=(self.username, self.password,),
            timeout=(self.timeout, self.timeout,),
            verify=False
        )
        return response


def check_api_response_on_error(response: dict) -> Optional[dict]:
    if 'result' in response and 'error' in response['result']:
        err: dict = response['result']['error']
        if err and err.get('status'):
            return err


class TicketResponseValidator:
    """ Class implement methods for check external api response on access for pay """
    def __init__(self, response: dict) -> None:
        self.response_data: dict = response.get('result')

    @staticmethod
    def _set_payment_state(ticket: dict) -> None:
        if not ticket:
            return

        available_inn = TerminalsPaymo.objects.filter(
            inn__isnull=False, api_key__isnull=False, is_active=True).values_list('inn', flat=True)
        if ticket.get('inn') and ticket.get('inn') not in available_inn:
            ticket['paymentEnabled'] = False
            return

        today = datetime.today().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        date_bn = ticket.get('DateBN', None)
        if date_bn:
            available_date = datetime.fromisoformat(str(date_bn)).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
            if today < available_date:
                ticket['paymentEnabled'] = False
                return

    def validate(self) -> None:
        try:
            if 'ticketsList' in self.response_data:
                ticket_list: list = self.response_data.get('ticketsList')
                for ticket in ticket_list:
                    self._set_payment_state(ticket)
            else:
                self._set_payment_state(self.response_data)
        except Exception as e:
            logger.exception(e)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}'
