from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from payments.models import Payment
from account.serializers import ProfileSerializer


class PaymentSerializer(ModelSerializer):
    user = ProfileSerializer(required=False)

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(PaymentSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        if self.request_user:
            validated_data['user'] = self.request_user
        return super().create(validated_data)

    class Meta:
        model = Payment
        fields = '__all__'
