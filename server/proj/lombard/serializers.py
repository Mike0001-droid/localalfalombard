from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from lombard.models import Favorites, Page


class FavoritesSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(FavoritesSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        if self.request_user:
            validated_data['user'] = self.request_user
        return super().create(validated_data)

    class Meta:
        model = Favorites
        fields = '__all__'


class PageSerializer(ModelSerializer):

    class Meta:
        model = Page
        fields = '__all__'
