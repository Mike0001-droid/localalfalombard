from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status

from lombard import service, schemas
from lombard.models import Favorites, Page
from lombard.serializers import FavoritesSerializer, PageSerializer


class LombardViewSet(ViewSet):
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
    """

    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)
    schema = schemas.LombardSchema()

    @action(detail=False, methods=['post'])
    def get_tickets(self, request):
        params = request.data
        try:
            result = self.service.get_tickets(**params)
            favorites = Favorites.objects.filter(user=request.user)
        except (KeyError, AttributeError) as e:
            raise e
            return Response({"error": f'Ошибка в валидации ответа 1С: {e}'}, status.HTTP_400_BAD_REQUEST)
        except NotImplementedError:
            return Response({'error': 'Метод не найден'}, status=status.HTTP_400_BAD_REQUEST)
        except service.ServiceError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        except service.SettingsSiteError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST) 
        serializer = FavoritesSerializer(favorites, request_user=request.user, many=True)
        result['favorites'] = serializer.data
        return Response(result)

    @action(detail=False, methods=['post'])
    def get_ticket_info(self, request):
        params = request.data
        try:
            result = self.service.get_ticket_info(**params)
        except NotImplementedError as e:
            return Response({
                'error': 'Метод не найден',
            }, status=status.HTTP_400_BAD_REQUEST)
        except service.ServiceError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        except service.SettingsSiteError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)

    @action(detail=False, methods=['post'])
    def get_ticket_accrual(self, request):
        params = request.data
        try:
            result = self.service.get_ticket_accrual(**params)
        except NotImplementedError as e:
            return Response({
                'error': 'Метод не найден',
            }, status=status.HTTP_400_BAD_REQUEST)
        except service.ServiceError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        except service.SettingsSiteError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)

    @action(detail=False, methods=['post'])
    def get_debt(self, request):
        params = request.data
        try:
            result = self.service.get_debt(**params)
        except NotImplementedError as e:
            return Response({
                'error': 'Метод не найден',
            }, status=status.HTTP_400_BAD_REQUEST)
        except service.ServiceError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        except service.SettingsSiteError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)

    @action(detail=False, methods=['post'])
    def get_tickets_sum(self, request):
        params = request.data
        try:
            result = self.service.get_tickets_sum(**params)
        except NotImplementedError as e:
            return Response({
                'error': 'Метод не найден',
            }, status=status.HTTP_400_BAD_REQUEST)
        except service.ServiceError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        except service.SettingsSiteError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)

    @action(detail=False, methods=['post'])
    def get_tickets_ending(self, request):
        try:
            result = self.service.get_tickets_ending()
        except NotImplementedError as e:
            return Response({
                'error': 'Метод не найден',
            }, status=status.HTTP_400_BAD_REQUEST)
        except service.ServiceError as e:
            return Response({'error': e.jsn}, status=status.HTTP_400_BAD_REQUEST)
        except service.SettingsSiteError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        
        return Response(result)

    @property
    def service(self):
        if not hasattr(self, '__service'):
            setattr(self, '__service', service.LombardService())
        return getattr(self, '__service')


class FavoritesViewSet(GenericViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = (IsAuthenticated,)
    schema = schemas.FavoritesSchema()

    def list(self, request, *args, **kwargs):
        favorites = Favorites.objects.filter(user=request.user)
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def pin(self, request):
        try:
            ticket = Favorites.objects.get(ticket=request.data.get('ticket'), user=request.user)
            serializer = self.get_serializer(ticket, request_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Favorites.DoesNotExist:
            params = request.data
            params['user'] = request.user.id
            serializer = self.get_serializer(data=params, request_user=request.user)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def unpin(self, request):
        try:
            ticket = Favorites.objects.filter(ticket=request.data.get('ticket'), user=request.user)
            ticket.delete()
            return Response(status=status.HTTP_200_OK)
        except Favorites.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PageViewSet(GenericViewSet):
    queryset = Page.objects.all()
    lookup_field = 'slug'
    serializer_class = PageSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
