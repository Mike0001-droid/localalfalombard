from django.db import models
from account.models import Profile


class Payment(models.Model):
    STATUS = (
        (0, 'CREATED'),
        (1, 'PENDING'),
        (2, 'SUCCEEDED'),
        (3, 'FAILED'),
        (4, 'REFUNDED'),
    )
    order_id = models.AutoField('Номер оплаты в системе', primary_key=True)
    ticket_id = models.UUIDField('Идентификатор залогового билета в 1С', null=True, blank=True, db_index=True)
    inn = models.CharField('ИНН', max_length=12, null=True, blank=True)
    ticket = models.CharField('Номер залогового билета', null=True, max_length=255, blank=True)
    user = models.ForeignKey(Profile, verbose_name='Пользователь', related_name='payments', on_delete=models.DO_NOTHING)
    amount = models.DecimalField('Сумма к оплате', max_digits=128, decimal_places=2)
    debt_amount = models.DecimalField('Сумма к оплате по процентам', max_digits=128, decimal_places=2, default=0)
    penalty_amount = models.DecimalField('Сумма к оплате по пеням', max_digits=128, decimal_places=2, default=0)
    loan_amount = models.DecimalField('Сумма к оплате по телу займа', max_digits=128, decimal_places=2, default=0)
    ip = models.CharField('IP запроса', max_length=255, null=True, blank=True)

    payment_id = models.CharField('Номер платежа', max_length=63, null=True, blank=True, db_index=True)
    transaction_id = models.CharField('Уникальный идентификатор транзакции', max_length=63, null=True, blank=True)
    md_order = models.CharField('Уникальный идентификатор операции на ПШ',  max_length=63, null=True, blank=True)
    auth_code = models.CharField('Код авторизации', max_length=7, null=True, blank=True)
    error_code = models.PositiveIntegerField('Код ошибки', null=True, blank=True)
    error_message = models.TextField('Сообщение ошибки', null=True, blank=True)
    status = models.PositiveSmallIntegerField('Статус', choices=STATUS, default=0, db_index=True)
    details = models.JSONField('Детали', blank=True, null=True)

    exported = models.BooleanField('Отправлена ли оплата в 1С', default=False)
    created = models.DateTimeField('Создано', auto_now_add=True, db_index=True)
    updated = models.DateTimeField('Изменено', auto_now=True, db_index=True)

    def __str__(self):
        return '{}: {}'.format(self.order_id, self.get_status_display())

    class Meta:
        ordering = ['-created']
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class LogEntry(models.Model):
    order_id = models.ForeignKey(Payment, verbose_name='Идентификатор оплаты', related_name='logs',
                                 db_index=True, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField('ИД транзакции банка', max_length=63, null=True, blank=True, db_index=True)
    method = models.CharField('Метод', max_length=100, db_index=True)
    request_text = models.TextField('Текст запроса', null=True, blank=True)
    response_text = models.TextField('Текст ответа', null=True, blank=True)
    created = models.DateTimeField('Создано', auto_now_add=True, db_index=True)

    def __str__(self):
        return '{}'.format(self.transaction_id if self.transaction_id else self.order_id)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Запись в журнале'
        verbose_name_plural = 'Записи в журнале'


class TerminalsPsbank(models.Model):
    inn = models.CharField('ИНН', max_length=12)

    bank_key_1 = models.CharField('Секретный ключ №1', max_length=50, help_text='bank_key_1')
    bank_key_2 = models.CharField('Секретный ключ №2', max_length=50, help_text='bank_key_1')
    terminal = models.PositiveBigIntegerField('Номер терминала организации', help_text='terminal')
    merchant = models.PositiveBigIntegerField('Номер организации', help_text='merchant')
    merch_name = models.CharField('Название организации', max_length=30, help_text='merch_name')
    trtype = models.PositiveSmallIntegerField('Тип запрашиваемой операции', help_text='trtype')

    return_url = models.CharField('return url', max_length=255, null=True,
                                  help_text='Ссылка для возвращения с сайта банка. /api/payments/result/')
    notify_url = models.CharField('notify url', max_length=255, null=True, help_text='/api/payments/check/')
    notify_email = models.EmailField('Емайл уведомлений', null=True)
    is_test = models.BooleanField('Тестовый режим', default=False)
    is_active = models.BooleanField('Включён', default=True,
                                    help_text='Включён. Если отключить, то терминал будет деактивирован '
                                              'и не будет учитываться системой')

    def __str__(self):
        return f'{self.inn}: {self.merch_name}'

    class Meta:
        verbose_name = 'Терминал ПСБанк'
        verbose_name_plural = 'Терминал ПСБанк'


class TerminalsPaymo(models.Model):
    inn = models.CharField('ИНН', max_length=12)
    api_key = models.CharField('Апи ключ для суммы меньше порога', max_length=50, help_text='Api-Key')
    api_key_above = models.CharField('Апи ключ для суммы больше порога', max_length=50, help_text='Api-Key',
                                     null=True, blank=True)
    secret = models.CharField('Секретный ключ для суммы меньше порога', max_length=50)
    secret_above = models.CharField('Секретный ключ для суммы больше порога', max_length=50, null=True, blank=True)
    threshold = models.FloatField('Порог цены', default=2000)
    is_active = models.BooleanField('Включён', default=True,
                                    help_text='Включён. Если отключить, то терминал будет деактивирован '
                                              'и не будет учитываться системой')

    def __str__(self):
        return f'{self.inn}: {self.is_active}'

    class Meta:
        verbose_name = 'Терминал Paymo'
        verbose_name_plural = 'Терминал Paymo'
