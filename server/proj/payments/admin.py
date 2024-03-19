from django.contrib import admin
from payments.models import Payment, LogEntry, TerminalsPsbank, TerminalsPaymo


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'transaction_id', 'inn', 'amount', 'status', 'created', 'updated')


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'transaction_id', 'method', 'created')
    list_display_links = ('order_id', 'transaction_id')
    list_filter = ('method',)

# @admin.register(TerminalsPsbank)
# class TerminalsPsbankAdmin(admin.ModelAdmin):
#     list_display = ('inn', 'merchant', 'merch_name', 'trtype', 'is_return_url', 'is_test', 'is_active')
#
#     def is_return_url(self, obj):
#         return bool(obj.return_url)
#     is_return_url.boolean = True
#     is_return_url.short_description = 'return_url'


@admin.register(TerminalsPaymo)
class TerminalsPaymoAdmin(admin.ModelAdmin):
    list_display = ('inn', 'api_key_hidden', 'api_key_above_hidden', 'threshold', 'is_active',)
    list_editable = ('threshold',)

    def api_key_hidden(self, obj):
        if not obj.api_key:
            return ''
        return f'{obj.api_key[:5]} . . . . . {obj.api_key[-5:]}'
    api_key_hidden.short_description = 'api_key меньше порога'

    def api_key_above_hidden(self, obj):
        if not obj.api_key_above:
            return ''
        return f'{obj.api_key_above[:5]} . . . . . {obj.api_key_above[-5:]}'
    api_key_above_hidden.short_description = 'api_key больше порога'
