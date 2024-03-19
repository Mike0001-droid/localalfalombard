from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from django.db.models import Q

from account.models import Profile, FormMessage, SiteInfo


class ProfileCreateSerializer(ModelSerializer):
    password_confirm = serializers.CharField()

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return Profile.objects.create_user(**validated_data)

    def validate(self, attrs):
        password = attrs.get("password", None)
        password_confirm = attrs.get("password_confirm", None)

        if password_confirm != password:
            raise serializers.ValidationError(
                {"password_confirm": ["Пароли не совпадают"]})

        return super(ProfileCreateSerializer, self).validate(attrs)

    class Meta:
        model = Profile
        fields = ['client_id', 'email', 'phone', 'password', 'password_confirm', 'fio']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ProfileSerializer(ModelSerializer):
    client_id = serializers.CharField(read_only=True)
    # phone = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = ('client_id', 'email', 'notify', 'phone', 'fio')


class FormMessageSerializer(ModelSerializer):

    class Meta:
        model = FormMessage
        fields = '__all__'


class TokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            user = Profile.objects.get(
                Q(email__iexact=attrs[self.username_field]) | Q(phone__iexact=attrs[self.username_field]))
        except Profile.DoesNotExist:
            raise exceptions.AuthenticationFailed("Пользователь не найден", "authentication_failed")
        except Exception:
            raise exceptions.AuthenticationFailed("Ошибка поиска пользователя - MultipleObjectsReturned", "authentication_failed")
        if user.check_password(attrs["password"]):
            refresh = self.get_token(user)

            data = dict()
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
            return data
        else:
            raise exceptions.AuthenticationFailed("Пароль не верен", "authentication_failed")

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['client_id'] = user.email
        return token


class SiteInfoSerializer(ModelSerializer):

    class Meta:
        model = SiteInfo
        fields = ('phone', 'email', 'footer_text')
