from rest_framework.schemas import AutoSchema
import coreapi
import coreschema


class ProfileSchema(AutoSchema):

    def get_serializer_fields(self, path, method):
        if method == 'POST' and path.endswith('/create_user/'):
            return [
                coreapi.Field(
                    name='client_id',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Идентификатор клиента в 1С')
                ),
                coreapi.Field(
                    name='email',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Email')
                ),
                coreapi.Field(
                    name='phone',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Телефон')
                 ),
                coreapi.Field(
                    name='password',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Пароль')
                 ),
                coreapi.Field(
                    name='password_confirm',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Пароль (повторный)')
                 ),
            ]
        elif method == 'POST' and path.endswith('/check_user/'):
            return [
                coreapi.Field(
                    name='phone',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Телефон')
                ),
                coreapi.Field(
                    name='series',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Серия паспорта')
                ),
                coreapi.Field(
                    name='number',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Номер паспорта')
                )
            ]
        elif method == 'POST' and path.endswith('/update_user/'):
            return [
                coreapi.Field(
                    name='email',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Email')
                ),
                coreapi.Field(
                    name='phone',
                    location='form',
                    required=False,
                    schema=coreschema.String(description='Телефон')
                ),
                coreapi.Field(
                    name='notify',
                    location='form',
                    required=True,
                    schema=coreschema.Boolean(description='Оповещения')
                )
            ]
        elif method == 'POST' and path.endswith('/update_password/'):
            return [
                coreapi.Field(
                    name='password',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Старый пароль')
                ),
                coreapi.Field(
                    name='password_new',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Новый пароль')
                ),
                coreapi.Field(
                    name='password_confirm',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Новый пароль подтвердить')
                ),
            ]
        elif method == 'POST' and path.endswith('/password_reset_user/'):
            return [
                coreapi.Field(
                    name='email',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Email')
                ),
            ]
        elif method == 'POST' and path.endswith('/ask_question/'):
            return [
                coreapi.Field(
                    name='email',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Email')
                ),
                coreapi.Field(
                    name='person',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Имя пользователя')
                ),
                coreapi.Field(
                    name='phone',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Телефон пользователя')
                ),
                coreapi.Field(
                    name='question',
                    location='form',
                    required=True,
                    schema=coreschema.String(description='Вопрос(комментарий)')
                ),
            ]
        return super().get_serializer_fields(path, method)

