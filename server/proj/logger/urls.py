from rest_framework import routers
from logger.views import LogViewSet


router = routers.DefaultRouter()
router.register(r'log', LogViewSet, basename='log')

app_name = 'logger'
urlpatterns = router.urls
