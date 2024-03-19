from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.serializers import TokenSerializer
from account.views import ProfileViewSet

router = routers.DefaultRouter()

router.register(r'', ProfileViewSet, basename='user')

app_name = 'account'
urlpatterns = router.urls
urlpatterns += [
    path('token/create/', TokenObtainPairView.as_view(serializer_class=TokenSerializer), name='token_auth'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
