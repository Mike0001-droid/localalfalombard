from rest_framework.schemas import AutoSchema, ManualSchema
import coreapi
import coreschema


class LombardSchema(AutoSchema):

    def get_serializer_fields(self, path, method):

        if path.endswith('/get_tickets/'):
            return [
                coreapi.Field(
                    name='client_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор клиента в 1С'),
                ),
                coreapi.Field(
                    name='status',
                    location='form',
                    required=False,
                    schema=coreschema.Number(description='Статус залоговых билетов (default 0)'
                                                   '<br>0 — Все билеты'
                                                   '<br>1 — Активные билеты'
                                                   '<br>2 — Просроченные билеты'
                                                   '<br>3 — Выкупленные билеты'
                                                   '<br>4 — Билеты, ушедшие на аукцион'),
                ),
            ]

        if path.endswith('/get_ticket_info/'):
            return [
                coreapi.Field(
                    name='client_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор клиента в 1С'),
                ),
                coreapi.Field(
                    name='ticket_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
            ]

        if path.endswith('/get_ticket_accrual/'):
            return [
                coreapi.Field(
                    name='client_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор клиента в 1С'),
                ),
                coreapi.Field(
                    name='ticket_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
            ]

        if path.endswith('/get_debt/'):
            return [
                coreapi.Field(
                    name='client_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор клиента в 1С'),
                ),
                coreapi.Field(
                    name='ticket_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
                coreapi.Field(
                    name='date',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Расчетная дата, на момент наступления которой необходимо '
                                                         'рассчитать сумму процентов (формат: YYYY-MM-DD)'),
                ),
            ]

        # Дефолтнафя схема
        return [
            coreapi.Field(
                name='client_id',
                location='form',
                required=True,
                schema=coreschema.String(description='Идентификатор клиента в 1С')
            ),
        ]


class FavoritesSchema(AutoSchema):

    def get_serializer_fields(self, path, method):

        if path.endswith('/pin/'):
            return [
                coreapi.Field(
                    name='ticket',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
            ]
        elif path.endswith('/unpin/'):
            return [
                coreapi.Field(
                    name='ticket',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор залогового билета в 1С'),
                ),
            ]
        return super().get_serializer_fields(path, method)
