from rest_framework.schemas import AutoSchema, ManualSchema
import coreapi
import coreschema


class PaymentSchema(AutoSchema):

    def get_serializer_fields(self, path, method):

        if path.endswith('/pay/') or path.endswith('/pay_aft/'):
            return [
                coreapi.Field(
                    name='ticket',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Номер залогового билета'),
                ),
                coreapi.Field(
                    name='ticket_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
                coreapi.Field(
                    name='amount',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Сумма к оплате'),
                ),
                coreapi.Field(
                    name='date',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Расчетная дата, на момент наступления которой необходимо '
                                                         'рассчитать сумму процентов (формат: YYYY-MM-DD)'),
                ),
                 coreapi.Field(
                    name='loan_date',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Дата оформления залогового билета'),
                ),
            ]
        elif path.endswith('/result/'):
            return [
                coreapi.Field(
                    name='order',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='идентификатор оплаты'),
                ),
                coreapi.Field(
                    name='ticket',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Номер залогового билета'),
                ),
                coreapi.Field(
                    name='ticket_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
                coreapi.Field(
                    name='amount',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Сумма к оплате'),
                ),
            ]
        elif path.endswith('/check/'):
            return [
                coreapi.Field(
                    name='ticket',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
            ]
        return super().get_serializer_fields(path, method)
