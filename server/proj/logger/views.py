from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

import coreapi
import coreschema
import logging

from django.conf import settings
DEBUG = settings.DEBUG


schema = ManualSchema(
    fields=[
        coreapi.Field(
            name='message',
            required=True,
            location='form',
            schema=coreschema.String(description='Сообщение'),
        ),
        coreapi.Field(
            name='level',
            required=False,
            location='form',
            schema=coreschema.Enum(enum=('debug', 'info', 'warning', 'error', 'critical',), description='Уровень логирования'),
        ),
        coreapi.Field(
            name='channel',
            required=False,
            location='form',
            schema=coreschema.Enum(enum=('main',), description='Канал для отправки'),
        ),
    ],
    encoding='application/json',
    description='Отправка записи лога'
)

PermissionsClass = AllowAny


class LogViewSet(ViewSet):
    permission_classes = (PermissionsClass,)

    @action(methods=['post'], detail=False, schema=schema)
    def send(self, request):
        params = request.data

        message = params.get('message')
        if not message:
            return Response({ 'detail': 'message должен быть определен', }, status=400)

        level = params.get('level', 'debug')
        if not isinstance(getattr(logging, level.upper(), None), int):
            return Response({'detail': 'Недопустимое значение level', }, status=400)

        channel = params.get('channel', 'main')
        if channel not in ('main',):
            return Response({'detail': 'Недопустимое значение channel', }, status=400)

        try:
            logger = logging.getLogger('logger.' + channel)
            loglevel = getattr(logging, level.upper(), 0)
            logger.log(loglevel, message)
            return Response({'ok': True, })
        except Exception as e:
            return Response({'detail': 'Не удалось отправить запись: %s' % (str(e),), }, status=500)
