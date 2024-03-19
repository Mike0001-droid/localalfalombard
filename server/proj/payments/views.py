from typing import Union

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from lombard.service import LombardService, ServiceError as LombardError
from payments.schemas import PaymentSchema
from payments.serializers import PaymentSerializer, Payment
from payments.service import BankService


class PaymentViewSet(ViewSet):
    """
        Методы для работы с платежной системой
        pay:
            Получение платежной ссылки для перехода на Платежный Шлюз
        check:
            Запрос проверки статуса платежа предназначенный для notify_url получаемый от банка
        result:
            Проверка платежа по билету и номеру заказа
        pay_aft:
            Получение параметров платежа, для генерации формы с POST запросом и последущим переходом
            (без preventDefault) на https://test.3ds.payment.ru/cgi-bin/cgi_link.
    """
    schema = PaymentSchema()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def pay(self, request, *args, **kwargs):
        try:
            payment = self._register(request, *args, **kwargs)
            if payment and payment.get('order_id'):
                data = request.data
                result = self.bank.create_payment_link(
                    amount=float(payment.get('amount', 0)),
                    order_id=payment.get('order_id'),
                    inn=payment.get('inn'),
                    ticket=payment.get('ticket'),
                    host=request.META.get('HTTP_ORIGIN', ''),
                    user=request.user,
                    data=data
                )
                return Response(result, status=status.HTTP_200_OK)
            elif payment and payment.status_code and payment.status_code > 200:
                return payment
            else:
                return Response({'error': 'Произошла неизвестная ошибка', 'detail': 'Произошла неизвестная ошибка'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e), 'detail': 'Ошибка с оплатой'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def pay_psbank(self, request, *args, **kwargs):
        params = request.data
        params['amount'] = float(params.get('amount', 0))

        try:
            payment = self._register(request, *args, **kwargs)
            if payment and payment.get('order_id'):
                result = self.bank.create_payment_link(request=request, payment=payment, **params)
                return Response(result, status=status.HTTP_200_OK)
            elif payment and payment.status_code and payment.status_code > 200:
                return payment
            else:
                return Response({'error': 'Произошла неизвестная ошибка', 'detail': 'Произошла неизвестная ошибка'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e), 'detail': 'Ошибка с оплатой'}, status=status.HTTP_400_BAD_REQUEST)
    """
        PSB check

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def check(self, request, *args, **kwargs):
        params = request.data
        params['amount'] = float(params.get('amount', 0))
        payment = Payment.objects.filter(amount=params.get('AMOUNT'), order_id=params.get('ORDER')[5:])
        if payment and params.get('P_SIGN'):
            if payment.status in [0, 1]:
                result = self.bank.check(payment=payment, request=request, **params)
                if not payment.exported and payment.status in [0, 1]:
                    self._update_payment(payment, result)
        return Response(status=status.HTTP_200_OK)
    """
    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def result(self, request, *args, **kwargs):
        params = request.data or request.query_params.copy()
        params['amount'] = float(params.get('amount', 0))
        try:
            payment = Payment.objects.filter(ticket_id=params.get('ticket_id'), order_id=params.get('order')).last()
            if payment:
                if payment.status in [2] and payment.transaction_id:
                    return Response({
                        'status': 0,
                        'detail': f'Оплата по залоговому билету № {payment.ticket} прошла успешно'
                    }, status=status.HTTP_200_OK)
                elif payment.status in [0, 1]:
                    result = self.bank.check_result(payment=payment, **params)
                    if not payment.exported and payment.status in [0, 1]:
                        self._update_payment(payment, result)
                    if result:
                        return Response({
                            'status': 0,
                            'detail': f'Оплата по залоговому билету № {payment.ticket} прошла успешно'
                        }, status=status.HTTP_200_OK)
                return Response({'error': f'Оплату по залоговому билету № {payment.ticket} произвести не удалось'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e), }, status=status.HTTP_400_BAD_REQUEST)

    """
        PSB result

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def result_psbank(self, request, *args, **kwargs):
        params = request.data or request.query_params.copy()
        params['amount'] = float(params.get('amount', 0))

        try:
            payment = Payment.objects.filter(ticket_id=params.get('ticket_id'), order_id=params.get('order')).last()

            if payment:
                if payment.status in [2] and payment.transaction_id:
                    return Response({
                        'status': 0,
                        'detail': f'Оплата по залоговому билету № {payment.ticket} прошла успешно'
                    }, status=status.HTTP_200_OK)
                elif payment.status in [0, 1]:
                    result = self.bank.check_result(payment=payment, request=request, **params)
                    if not payment.exported and payment.status in [0, 1]:
                        self._update_payment(payment, result)
                    if result:
                        return Response({
                            'status': 0,
                            'detail': f'Оплата по залоговому билету № {payment.ticket} прошла успешно'
                        }, status=status.HTTP_200_OK)
                return Response({'error': f'Оплату по залоговому билету № {payment.ticket} произвести не удалось'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e), }, status=status.HTTP_400_BAD_REQUEST)
    """

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def pay_aft(self, request, *args, **kwargs):
        params = request.data
        params['amount'] = float(params.get('amount', 0))

        try:
            payment = self._register(request, *args, **kwargs)
            if payment and payment.get('order_id'):
                result = self.bank.create_payment_params(request=request, payment=payment, **params)
                return Response(result, status=status.HTTP_200_OK)
            elif payment and payment.status_code and payment.status_code > 200:
                return payment
            else:
                return Response({'error': 'Произошла неизвестная ошибка', }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e), }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def start_callback(self, request, *args, **kwargs):
        params = request.data or request.query_params.copy()
        self.bank.start_callback(params=params)
        return Response({'result': True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def finish_callback(self, request, *args, **kwargs):
        params = request.data or request.query_params.copy()
        try:
            result = self.bank.finish_callback(params=params, bank_signature=params.get('signature'))
            self._update_payment(payment=result.get('payment'), result=params)
            return Response(result.get('response'), status=status.HTTP_200_OK)
        except LombardError as e:
            return Response(e.jsn, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @property
    def lombard(self):
        if not hasattr(self, '__lombard'):
            setattr(self, '__lombard', LombardService())
        return getattr(self, '__lombard')

    @property
    def bank(self):
        if not hasattr(self, '__bank'):
            setattr(self, '__bank', BankService())
        return getattr(self, '__bank')

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        else:
            return request.META.get('REMOTE_ADDR')

    def _register(self, request: Request, *args, **kwargs) -> Union[dict, Response]:
        # регистрация оплаты в 1с
        params = request.data
        amount = float(params.get('amount', 0))

        if not amount:
            text = 'Сумма к оплате неверна или отсутствует'
            return Response({'detail': text, 'error': {'amount': text}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            debt_object = self.lombard.get_debt(client_id=request.user.client_id, **params)
        except NotImplementedError:
            return Response({'error': 'Метод не найден'}, status=status.HTTP_400_BAD_REQUEST)
        except LombardError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        debt = debt_object.get('result')
        debt_amount = float(debt.get('debtSum'))
        penalty_amount = float(debt.get('debtPenySum', 0))
        loan_amount = float(round((amount - debt_amount) * 100) / 100)
        inn = debt.get('inn') or params.pop('inn', None)

        if amount < debt_amount:
            text = 'Сумма к оплате не может быть меньше долга по процентам'
            return Response({'detail': text, 'error': {'amount': text}}, status=status.HTTP_400_BAD_REQUEST)

        if not debt.get('paymentEnabled'):
            text = f'Платеж по залоговому билету № {params.get("ticket")} невозможен'
            return Response({'detail': text, 'error': {'amount': text}}, status=status.HTTP_400_BAD_REQUEST)

        if not inn:
            text = f'Платеж по залоговому билету № {params.get("ticket")} невозможен, ИНН не обнаружен'
            return Response({'detail': text, 'error': {'inn': text}}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= debt_amount + float(debt.get('maxBodySum')):
            serializer = PaymentSerializer(request_user=request.user, data={
                'debt_amount': round(debt_amount-penalty_amount, 2),
                'loan_amount': loan_amount,
                'penalty_amount': penalty_amount,
                'ip': self.get_client_ip(request),
                'inn': inn,
                **params
            })

            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _update_payment(self, payment, result):
        if payment and payment.order_id and result:
            params = dict()
            if self.action == 'finish_callback':
                params = {
                    'auth_code': result.get('auth_code', None),
                    'payment_id': result.get('payment_id', None),
                    'transaction_id': result.get('tx_id', None),
                    'md_order': result.get('md_order', None),
                    'error_code': result.get('error_code', None),
                    # 'error_message': result.get('RCTEXT', None),
                    'details': str(result),
                }
                if result.get('result', False):
                    payment_status = result.get('invoice_status', '')
                    if payment_status == 'deposited':
                        params.update(status=2)
                    elif payment_status == 'processing':
                        params.update(status=1)
                else:
                    params.update(status=3)
            else:
                if result.get('result', None) == 'success':
                    payment_status = result.get('status', '')
                    if payment_status == 'deposited':
                        params['status'] = 2
                    elif payment_status == 'processing':
                        params['status'] = 1
                else:
                    params['status'] = 3

            serializer = PaymentSerializer(payment, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if not payment.exported and not serializer.data.get('exported') and serializer.data.get('status') == 2:
                self.lombard.online_pay(
                    client_id=payment.user.client_id,
                    **serializer.data
                )
                payment.exported = True
                payment.save()
        elif payment and payment.order_id:
            payment.status = 3
            payment.save()
