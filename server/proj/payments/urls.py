from django.urls import path
from rest_framework import routers

from payments.views import PaymentViewSet

router = routers.DefaultRouter()

router.register(r'', PaymentViewSet, basename='payments')

app_name = 'payments'
urlpatterns = router.urls
