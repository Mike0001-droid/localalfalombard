from django.urls import path
from rest_framework import routers

from lombard.views import LombardViewSet, FavoritesViewSet, PageViewSet

router = routers.DefaultRouter()

router.register(r'', LombardViewSet, basename='lombard')
router.register(r'favorites', FavoritesViewSet, basename='favorites')
router.register(r'pages', PageViewSet, basename='pages')

app_name = 'lombard'
urlpatterns = router.urls
