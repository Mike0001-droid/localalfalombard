from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from account.models import Profile, SiteInfo
from account.schemas import ProfileSchema
from account.serializers import FormMessageSerializer, ProfileCreateSerializer, ProfileSerializer, \
    SiteInfoSerializer, TokenSerializer
from lombard.service import LombardService, ServiceError


class ProfileViewSet(ViewSet):
    """
    profile:
        Получение авторзированного профиля пользователя
    check_user:
        Проверка пользователя на наличие в 1С
    create_user:
        Создание пользователя
    update_user:
        Обновление пользователей
    password_reset_user:
        Восстановления пароля пользователя
    """
    schema = ProfileSchema()

    @action(detail=False)
    def profile(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def check_user(self, request):
        params = {
            'phone': request.data.get('phone', ''),
            'personDocument': {
                'series': request.data.get('series', ''),
                'number': request.data.get('number', ''),
            }
        }
        try:
            result = self.lombard.check_user_registration(**params)
        except NotImplementedError:
            return Response({
                'error': 'Метод не найден',
            }, status=status.HTTP_400_BAD_REQUEST)
        except ServiceError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = ProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token_data = {
            'email': request.data['email'],
            'password': request.data['password']
        }
        token_serializer = TokenSerializer(data=token_data)
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def update_user(self, request):
        # if 'email' in request.data:
        #     del request.data['email']
        if 'password' in request.data:
            del request.data['password']
            # request.data['password'] = make_password(request.data['password'])
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_password(self, request):
        try:
            user = self.request.user
            password = self.request.data.get('password')
            password_new = self.request.data.get('password_new')
            password_confirm = self.request.data.get('password_confirm')
            if user.check_password(password) and password_new == password_confirm:
                user.set_password(password_new)
                user.save(update_fields=['password'])
                return Response({'detail': 'Пароль успешно сохранен'},
                                status=status.HTTP_200_OK)
            elif not user.check_password(password):
                return Response(
                    {'detail': 'Неверный пароль', 'error': {'password': 'Неверный пароль'}},
                    status=status.HTTP_400_BAD_REQUEST)
            elif not password_new == password_confirm:
                text = 'Пароли не совпадают'
                return Response(
                    {'detail': text, 'error': {'password_new': text}},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                text = 'Произошла неизвестная ошибка'
                return Response(
                    {'detail': text, 'error': {'password': text}},
                    status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            text = 'Пользователь не найден'
            return Response({'detail': text, 'error': {'user': text}}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def password_reset_user(self, request):
        if 'email' in request.data:
            email = request.data.get('email')
            try:
                user = Profile.objects.get(email=email)
                password = Profile.objects.make_random_password()
                user.set_password(password)
                user.save(update_fields=['password'])
                message = 'Запрос на восстановление пароля \nНовый пароль сгенерирован: {password}'.format(
                    password=password)
                send_mail('Смена пароля', message, settings.EMAIL_HOST_USER, [email])
                return Response({'detail': 'Новый пароль отправлен на емайл: {}'.format(email)},
                                status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                text = 'Пользователь с емайлом {}, не найден'.format(email)
                return Response({'detail': text, 'error': {'email': text}}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(
                    {'detail': 'Произошла неизвестная ошибка', 'error': {'email': 'Произошла неизвестная ошибка'}},
                    status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Не передан емайл', 'error': {'email': 'Не передан емайл'}},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def ask_question(self, request, *args, **kwargs):
        serializer = FormMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                html_body = render_to_string('ask_question.html', {'object': serializer.data})
                mail = EmailMultiAlternatives(
                    subject=f'Новый вопрос пользователя',
                    body=html_body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[
                        settings.DEFAULT_EMAIL
                    ]
                )
                mail.attach_alternative(html_body, 'text/html')
                mail.send()
            except Exception as e:
                return Response(f'Не удалось отправить сообщение: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_site_info(self, request):
        try:
            info = SiteInfo.objects.first()
            serializer = SiteInfoSerializer(info)
            return Response(serializer.data)
        except SiteInfo.DoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ('profile', 'update_user', 'update_password'):
            permission_classes = [IsAuthenticated]
        elif self.action in ('check_user', 'create_user', 'password_reset_user', 'ask_question', 'get_site_info'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @property
    def lombard(self):
        if not hasattr(self, '__lombard'):
            setattr(self, '__lombard', LombardService())
        return getattr(self, '__lombard')
