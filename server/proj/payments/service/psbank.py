import hmac
import requests
from datetime import datetime
from hashlib import sha256
from secrets import token_hex
from urllib.parse import urlencode, urlparse, parse_qsl

from utils.service import RESTService, ServiceError
from utils.transport.rest import check_api_response_on_error
from payments.models import Payment, LogEntry, TerminalsPsbank
from lombard.service import ExternalApiActions

import logging
logger = logging.getLogger('banking')


class BankService:
    """
        Ссылка на документацию
        https://www.psbank.ru/-/media/Files/Business/Acquiring/Internet/TechDoc/Interaction_procedure_standard.pdf
        register_payment:
            6. Генерация ссылки для выполнения операций «Оплата» или «Предавторизация»
    """
    BANK_URL_PROD = 'https://3ds.payment.ru/cgi-bin'
    BANK_URL_DEV = 'https://test.3ds.payment.ru/cgi-bin'

    terminals = None
    inn = None

    def __init__(self, *args, **kwargs):
        self.terminals = self.get_settings()

    def get_settings(self, inn: int = None, key: str = None):
        """ Получаем список терминалом из базы, если терминалы уже были получены, то берём их из памяти """

        if not self.terminals:
            trm_db = TerminalsPsbank.objects.filter(is_active=True)
            if not trm_db:
                raise Exception('Отсутствуют настройки терминалов подключения')
            return trm_db

        terminals_dict = {}
        for terminal in self.terminals:
            terminals_dict[terminal.inn] = {
                'inn': terminal.inn,
                'bank_key_1': terminal.bank_key_1,
                'bank_key_2': terminal.bank_key_2,
                'terminal': terminal.terminal,
                'merchant': terminal.merchant,
                'merch_name': terminal.merch_name,
                'trtype': terminal.trtype,
                'notify_url': terminal.notify_url,
                'return_url': terminal.return_url,
                'notify_email': terminal.notify_email,
                'is_test': terminal.is_test,
            }
        if inn not in terminals_dict.keys():
            raise KeyError(f'ИНН "{inn}", не найден в списке терминалов')
        elif inn and not key:
            raise KeyError(f'Не передан ключ "{key}", для терминала ИНН "{inn}"')
        elif key not in terminals_dict[inn].keys():
            raise KeyError(f'Не найден ключ "{key}", для терминала ИНН "{inn}"')
        elif inn and key:
            return terminals_dict[inn][key]
        return terminals_dict

    default_session_timeout = 1200
    default_currency = 'RUB'

    def create_payment_link(self, request, amount: int, payment, inn: int, ticket: str = None, **kwargs):
        self.inn = inn
        keys = ['AMOUNT', 'CURRENCY', 'TERMINAL', 'TRTYPE', 'BACKREF', 'ORDER']

        order = payment.get('order_id')
        params = {
            'AMOUNT': amount,
            'CURRENCY': self.default_currency,
            'ORDER': f'10000{order}',
            'DESC': f'Оплата по залоговому билету № {ticket}',
            'EMAIL': self.get_user_email(request),
            'BACKREF': self._return_url(request, order, inn),
            'MERCHANT_NOTIFY_EMAIL': self.get_settings(inn, 'notify_email'),

            'TERMINAL': self.get_settings(inn, 'terminal'),
            'MERCHANT': self.get_settings(inn, 'merchant'),
            'MERCH_NAME': self.get_settings(inn, 'merch_name'),
            'TRTYPE': self.get_settings(inn, 'trtype'),
            'NOTIFY_URL': self.get_settings(inn, 'notify_url'),
        }
        params['P_SIGN'] = self._generate_p_sign(keys, params)
        test = self.get_settings(inn, 'is_test')
        response = self._request(test, 'payment_ref/generate_payment_ref', **params)

        log = LogEntry.objects.create(
            method='payment_ref/generate_payment_ref',
            response_text=str(response),
            request_text=str(params))

        log.order_id = Payment.objects.filter(order_id=order).last()
        log.save()
        return response

    def create_payment_params(self, request, amount: int, payment, inn: int, ticket: str = None, **kwargs):
        self.inn = inn
        keys = ['AMOUNT', 'CURRENCY', 'ORDER', 'MERCH_NAME', 'MERCHANT', 'TERMINAL',
                'EMAIL', 'TRTYPE', 'TIMESTAMP', 'NONCE', 'BACKREF']

        order = payment.get('order_id')
        params = {
            'AMOUNT': float(amount),
            'CURRENCY': self.default_currency,
            'ORDER': f'10000{order}',
            'DESC': f'Оплата по залоговому билету № {ticket}',
            'EMAIL': self.get_user_email(request),
            'TIMESTAMP': datetime.now().strftime('%Y%m%d%H%M%S'),
            'NONCE': token_hex(32),
            'BACKREF': self._return_url(request, order, inn),

            'TERMINAL': self.get_settings(inn, 'terminal'),
            'MERCHANT': self.get_settings(inn, 'merchant'),
            'MERCH_NAME': self.get_settings(inn, 'merch_name'),
            'TRTYPE': self.get_settings(inn, 'trtype'),
            'NOTIFY_URL': self.get_settings(inn, 'notify_url')
        }
        params['P_SIGN'] = self._generate_p_sign(keys, params)

        log = LogEntry.objects.create(
            method='create_payment_params',
            request_text=str(params))
        log.order_id = Payment.objects.filter(order_id=order).last()
        log.save()
        return params

    def check_result(self, payment, request, **kwargs):
        keys = ['AMOUNT', 'CURRENCY', 'ORDER', 'MERCH_NAME', 'MERCHANT', 'TERMINAL', 'EMAIL', 'TRTYPE',
                'TIMESTAMP', 'NONCE', 'BACKREF']
        payment_db = Payment.objects.filter(order_id=payment.order_id).last()
        inn = payment_db.inn
        self.inn = inn

        params = {
            'AMOUNT': float(payment.amount),
            'CURRENCY': self.default_currency,
            'ORDER': f'10000{payment.order_id}',
            'DESC': f'Оплата по залоговому билету № {payment.ticket}',
            'EMAIL': self.get_user_email(payment),
            'BACKREF': self._return_url(request, payment.order_id, inn),
            'TIMESTAMP': datetime.now().strftime('%Y%m%d%H%M%S'),
            'NONCE': token_hex(32),
            # **settings.BANK_PARAMS
            'TERMINAL': self.get_settings(inn, 'terminal'),
            'MERCHANT': self.get_settings(inn, 'merchant'),
            'MERCH_NAME': self.get_settings(inn, 'merch_name'),
            'TRTYPE': self.get_settings(inn, 'trtype'),
            'NOTIFY_URL': self.get_settings(inn, 'notify_url')
        }
        params['P_SIGN'] = self._generate_p_sign(keys, params)
        test = self.get_settings(inn, 'is_test')
        response = self._request(test, 'check_operation/ecomm_check', **params)
        log = LogEntry.objects.create(
            method='check_operation/ecomm_check',
            response_text=str(response),
            request_text=str(params)
        )
        log.order_id = payment_db
        log.save()
        return response

    def check(self, request, **kwargs):
        keys = ['amount', 'currency', 'order', 'merch_name', 'merchant', 'terminal', 'email', 'trtype', 'timestamp',
                'nonce', 'backref', 'result', 'rc', 'rctext', 'authcode', 'rrn', 'int_ref']
        request_p_sign = request.data.pop('P_SIGN', None)
        p_sign = self._generate_p_sign(keys, request.data)
        if request_p_sign == p_sign:
            return request.data
        return None

    def _return_url(self, request, order_id, inn):
        params = request.data or request.query_params.copy()
        query = {
            'order': order_id,
            'ticket': params.get('ticket'),
            'ticket_id': params.get('ticket_id'),
            'amount': params.get('amount')
        }

        host = request.META.get('HTTP_ORIGIN', '')
        ticket_id = params.get('ticket_id')
        url = f'{host}/ticket/{ticket_id}'

        url_parts = urlparse(url if url else self.get_settings(inn, 'return_url'))
        query_params = dict(parse_qsl(url_parts.query))
        query_params.update(query)

        return url_parts._replace(query=urlencode(query_params)).geturl()

    @property
    def key_1(self):
        return self.get_settings(self.inn, 'bank_key_1')

    @property
    def key_2(self):
        return self.get_settings(self.inn, 'bank_key_2')

    @staticmethod
    def get_user_email(request):
        return request.user.email

    def _generate_key(self):
        return bytes(a ^ b for a, b in zip(bytes.fromhex(self.key_1), bytes.fromhex(self.key_2))).hex().upper()

    def _generate_p_sign(self, keys, params):
        values = ''
        for key in keys:
            if params[key.upper()]:
                values += f'{len(str(params[key.upper()]))}{params[key.upper()]}'
            else:
                values += '-'

        return hmac.new(bytes.fromhex(self._generate_key()), msg=values.encode(), digestmod=sha256).hexdigest().upper()

    def _request(self, test, path, **kwargs):
        url = self.BANK_URL_DEV if test else self.BANK_URL_PROD
        url = f'{url}/{path}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }

        logger.debug('Request PsbPay to URL %s with args: %s' % (url, str(kwargs),))

        response = requests.post(url, data=kwargs, headers=headers, verify=False)
        try:
            response.raise_for_status()
        except Exception as e:
            logger.warning('Failed PsbPay with status %s' % (str(e),))
            raise requests.HTTPError('Банк PsbPay ответил ошибкой', response.status_code)

        result = response.json()
        logger.debug('Response PsbPay: %s \n' % (str(result),))
        return result
