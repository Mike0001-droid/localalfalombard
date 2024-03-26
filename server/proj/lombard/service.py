from enum import Enum
from datetime import datetime
from django.conf import settings
from utils.service import RESTService, ServiceError, SettingsSiteError
from utils.transport.rest import check_api_response_on_error

ACTION_URI_PREFIX = settings.TRANSPORT_1C['LOMBARD_PATH'] + settings.TRANSPORT_1C['SERVICE_PATH']


class ExternalApiActions(Enum):
    CHECK_REGISTRATION = ACTION_URI_PREFIX + 'checkRegistration'
    GET_INFO_ON_PERCENT_AMOUNT = ACTION_URI_PREFIX + 'getDebt'
    GET_TICKET_ACCRUAL = ACTION_URI_PREFIX + 'getTicketAccrual'
    GET_TICKET_INFO = ACTION_URI_PREFIX + 'getTicketInfo'
    GET_TICKETS = ACTION_URI_PREFIX + 'getTickets'
    GET_TICKETS_ENDING = ACTION_URI_PREFIX + 'getTicketsEnding'
    GET_TICKETS_SUMMARY = ACTION_URI_PREFIX + 'getTicketsSum'
    ONLINE_PAY = ACTION_URI_PREFIX + 'onlinePay'


class LombardService(RESTService):
    """
        get_tickets:
            3.3.1 Получение списка залоговых билетов клиента

        get_ticket_info:
            3.3.2 Получение залогового билета клиента

        get_ticket_accrual:
            3.3.3 Получение информации по начислению процентов

        get_debt:
            3.3.4 Получение информации по сумме процентов

        get_tickets_sum:
            3.3.5 Получение информации общей информации по билетам

        check_user_registration:
            3.1.1 Проверка пользователя на наличии в 1С

        online_pay:
            3.4.1 Отправка в систему данных об оплате процентов или тела
    """

    def get_tickets(self, **kwargs) -> dict:
        result = self.call(ExternalApiActions.GET_TICKETS.value,
                           clientId=kwargs.get('client_id', ''),
                           status=kwargs.get('status', 0))
        err = check_api_response_on_error(result)
        if err and int(err['status']) not in [0, 2]:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result

    def get_ticket_info(self, **kwargs) -> dict:
        result = self.call(ExternalApiActions.GET_TICKET_INFO.value, clientId=kwargs.get('client_id', ''),
                           ticketId=kwargs.get('ticket_id', ''))
        err = check_api_response_on_error(result)
        if err and int(err['status']) != 0:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result

    def get_ticket_accrual(self, **kwargs) -> dict:
        result = self.call(ExternalApiActions.GET_TICKET_ACCRUAL.value,
                           clientId=kwargs.get('client_id', ''),
                           ticketId=kwargs.get('ticket_id', ''))
        err = check_api_response_on_error(result)
        if err and int(err['status']) != 0:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result

    def get_debt(self, **kwargs) -> dict:
        result = self.call(ExternalApiActions.GET_INFO_ON_PERCENT_AMOUNT.value, clientId=kwargs.get('client_id', ''),
                           ticketId=kwargs.get('ticket_id', ''),
                           debtDate=kwargs.get('date') or datetime.now().strftime('%Y-%m-%d'))
        err = check_api_response_on_error(result)
        if err and int(err['status']) > 5:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result

    def get_tickets_sum(self, **kwargs) -> dict:
        result = self.call(ExternalApiActions.GET_TICKETS_SUMMARY.value, clientId=kwargs.get('client_id', ''))
        err = check_api_response_on_error(result)
        if err and int(err['status']) != 0:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result

    def get_tickets_ending(self) -> list:
        result = self.call(ExternalApiActions.GET_TICKETS_ENDING.value)
        err = check_api_response_on_error(result)
        if err and int(err['status']) != 0:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result.get('result', {'ticketsList': []}).get('ticketsList', [])

    def check_user_registration(self, **kwargs):
        result = self.call(ExternalApiActions.CHECK_REGISTRATION.value, phoneNumber=kwargs.get('phone', ''),
                           personDocument=kwargs.get('personDocument', {}))
        err = check_api_response_on_error(result)
        if err and int(err['status']) != 0:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result

    def online_pay(self, **kwargs):
        result = self.call(
            ExternalApiActions.ONLINE_PAY.value,
            clientId=kwargs.get('client_id', ''),
            ticketId=kwargs.get('ticket_id', ''),
            paymentSum=float(kwargs.get('amount', 0)),
            paymentDebtSum=float(kwargs.get('debt_amount', 0)) + float(kwargs.get('penalty_amount', 0)),
            paymentLoanSum=float(kwargs.get('loan_amount', 0)),
            paymentDate=datetime.now().strftime('%Y-%m-%d'),
            transaction_id=kwargs.get('payment_id') or kwargs.get('transaction_id') or kwargs.get('order_id', ''),
        )
        err = check_api_response_on_error(result)
        if err and int(err['status']) != 0:
            raise ServiceError('Exception', jsn=err, code=err['status'])
        return result
