import requests
from urllib.parse import urlencode, urlparse, parse_qsl
from django.db.models import QuerySet

from payments.models import Payment, LogEntry, TerminalsPaymo
from account.models import Profile
from utils.service import ServiceError
from hashlib import sha256

import logging
logger = logging.getLogger('banking.paymo')


class BankService:
    api_key: str = 'e6ece619-7e6f-4fc3-a452-93aa5e0e78c6'
    url: str = 'https://paymo.ru/rest'

    payment_status = {
        'processing': 'Платеж в обработке',
        'deposited': 'Транзакция совершена успешно',
        'declined': 'Транзакция неуспешна',
        'wait_external': 'Ожидается подтверждение от внешней платежной системы',
        'refunded': 'Осуществлен полный возврат денежных средств',
        'approved': 'Денежные средства захолдированы, ожидается подтверждение платежа.',
    }

    invoice_status = {
        'save': 'Платеж создан',
        'processing': 'Платеж в обработке',
        'deposited': 'Транзакция совершена успешно',
        'declined': 'Транзакция неуспешна',
        'inactive': 'Транзакция неуспешна',
    }

    inn: str = None
    amount: float = 0
    terminals: QuerySet[TerminalsPaymo] = None

    def __init__(self, *args, **kwargs):
        self.terminals: QuerySet[TerminalsPaymo] = self.get_terminals()

    def create_payment_link(
            self,
            amount: float,
            order_id: int,
            inn: str,
            host: str,
            ticket: str,
            user: Profile,
            data: dict = None
    ) -> dict:
        try:
            payment = Payment.objects.get(order_id=order_id)
        except Payment.DoesNotExist:
            return {'error': True, 'detail': 'Заказ не найден'}

        self.inn = inn
        self.amount = amount
        params = {
            'price': amount,
            'order': str(order_id),
            'description': 'Оплата по залоговому билету № {ticket}'.format(ticket=ticket),
            'departure_type': 'url',
            'auto_return': 3,
            'extra': {
                'success_redirect': self._return_url(host, order_id, data),
                'fail_redirect':  f'{host}/fail/',
                'receipt': {
                    'taxationSystem': 0,
                    'positions': [
                        {
                            'tax': 6,
                            'name': position.get('name'),
                            'amount': position.get('amount'),
                            'quantity': 1,
                            'paymentMethod': 4,
                            'paymentSubject': 4
                        } for position in self._get_positions(payment=payment)
                    ],
                    'contact': user.email or user.phone
                }
            }
        }
        response = self._request('merchant/invoice/', params)

        LogEntry.objects.create(
            method='merchant/invoice/',
            response_text=str(response),
            request_text=str(params),
            order_id=payment
        )
        if 'url' in response:
            response['REF'] = response.get('url')
        return response

    def check_result(self, payment: Payment, **kwargs):
        self.inn = payment.inn
        params = {
            'order': str(payment.order_id),
            'price': float(payment.amount)
        }
        response = self._request('merchant/invoice/status/', params)
        LogEntry.objects.create(
            method='merchant/invoice/status/',
            response_text=str(response),
            request_text=str(params),
            order_id=payment
        )
        if 'status' in response:
            if response.get('status') != 'deposited':
                raise ServiceError(self.payment_status.get(response.get('status')))
            return response
        raise ServiceError('Статус платежа не удалось получить')

    def start_callback(self, params, **kwargs):
        LogEntry.objects.create(
            method='payments/start_callback/',
            request_text=str(params)
        )
        return True

    def finish_callback(self, params, bank_signature: str, **kwargs):
        response = {'result': True}
        payment = None
        try:
            payment = Payment.objects.get(order_id=params.get('order_id'))
            self.inn = payment.inn
            settings = self.get_settings()
            signature = self._get_callback_signature(
                secret=self._get_secret_key(settings=settings, amount=float(payment.amount)),
                amount=float(payment.amount),
                transaction_id=str(params.get('tx_id'))
            )

            if not bank_signature == signature:
                response.update(
                    result=False,
                    error=True,
                    detail='Подпись не совпадает',
                    bank_signature=bank_signature,
                    signature=signature
                )
        except Payment.DoesNotExist:
            response.update(result=False, error=True, detail='Заказ не найден')
        except Exception as e:
            response.update(result=False, error=True, detail=str(e))

        LogEntry.objects.create(
            method='payments/finish_callback/',
            response_text=str(response),
            request_text=str(params),
            transaction_id=params.get('payment_id', ''),
            order_id=payment
        )

        if response.get('error', False):
            raise ServiceError(str(response))

        return dict(payment=payment, response=response)

    def get_terminals(self) -> QuerySet[TerminalsPaymo]:
        if not self.terminals:
            terminals = TerminalsPaymo.objects.filter(is_active=True)
            if not terminals:
                raise Exception('Отсутствуют настройки терминалов подключения')
            return terminals
        return self.terminals

    def get_settings(self) -> TerminalsPaymo:
        """ Получаем список терминалом из базы, если терминалы уже были получены, то берём их из памяти """
        terminals_dict = {}
        for terminal in self.terminals:
            terminals_dict[terminal.inn] = terminal
        if self.inn not in terminals_dict.keys():
            raise KeyError(f'ИНН "{self.inn}", не найден в списке терминалов')
        return terminals_dict.get(self.inn)

    @staticmethod
    def _get_signature(api_key: str, secret: str, amount: float, order_id: str) -> str:
        if not api_key or not secret:
            raise KeyError(f'Не удалось сформировать подпись')
        params = [api_key, order_id, str(int(amount * 100)), secret]
        return sha256.new(''.join(params).encode()).hexdigest()

    @staticmethod
    def _get_callback_signature(secret: str, amount: float, transaction_id: str) -> str:
        if not secret:
            raise KeyError(f'Не удалось сформировать подпись')
        params = [transaction_id, str(int(amount * 100)), secret]
        return sha256.new(''.join(params).encode()).hexdigest()

    @staticmethod
    def _get_api_key(settings: TerminalsPaymo, amount: float) -> str:
        api_key: str = settings.api_key or settings.api_key_above
        threshold: float = settings.threshold
        if settings.api_key and amount < threshold:
            api_key = settings.api_key
        elif settings.api_key_above and amount >= threshold:
            api_key = settings.api_key_above
        return api_key

    @staticmethod
    def _get_secret_key(settings: TerminalsPaymo, amount: float) -> str:
        secret: str = settings.secret or settings.secret_above
        threshold: float = settings.threshold
        if settings.secret and amount < threshold:
            secret = settings.secret
        elif settings.secret_above and amount >= threshold:
            secret = settings.secret_above
        return secret

    @staticmethod
    def _get_positions(payment: Payment) -> list:
        positions = []
        debt_amount = float(payment.debt_amount)
        loan_amount = float(payment.loan_amount) 
        penalty_amount = float(payment.penalty_amount)
        if debt_amount:
            positions.append({
                'name': 'Проценты по займу № {ticket}'.format(ticket=payment.ticket),
                'amount': debt_amount,
            })
        if loan_amount:
            positions.append({
                'name': 'Возврат займа № {ticket}'.format(ticket=payment.ticket),
                'amount': loan_amount,
            })
        if penalty_amount:
            positions.append({
                'name': 'Пени по займу № {ticket}'.format(ticket=payment.ticket),
                'amount': penalty_amount,
            })
        return positions

    def _request(self, path: str, params: dict):
        url = self.url
        url = f'{url}/{path}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        settings = self.get_settings()
        api_key = self._get_api_key(settings=settings, amount=params.get('price'))
        params.update(
            api_key=api_key,
            signature=self._get_signature(
                api_key=api_key,
                secret=self._get_secret_key(settings=settings, amount=params.get('price')),
                amount=params.get('price'),
                order_id=params.get('order')
            )
        )

        logger.info('Request Paymo to URL %s with args: %s' % (url, str(params),))

        response = requests.post(url, json=params, headers=headers, verify=False)
        try:
            response.raise_for_status()
        except Exception as e:
            result = response.json()
            logger.debug('Response Paymo: %s \n' % (str(result),))
            logger.exception('Failed Paymo with status %s' % (str(e),))
            raise requests.HTTPError('Банк Paymo ответил ошибкой', response.status_code)

        result = response.json()
        logger.info('Response Paymo: %s \n' % (str(result),))
        return result

    @staticmethod
    def _return_url(host, order_id, params):
        query = {
            'order': order_id,
            'ticket': params.get('ticket'),
            'ticket_id': params.get('ticket_id'),
            'amount': params.get('amount')
        }

        ticket_id = params.get('ticket_id')
        url = f'{host}/ticket/{ticket_id}'

        url_parts = urlparse(url)
        query_params = dict(parse_qsl(url_parts.query))
        query_params.update(query)

        return url_parts._replace(query=urlencode(query_params)).geturl()
