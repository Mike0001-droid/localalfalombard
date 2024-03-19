from django.contrib import admin
from lombard.models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_publication', 'publication')
    search_fields = ('title', 'publication')
