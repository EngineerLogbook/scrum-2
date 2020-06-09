from django.contrib import admin
from .models import History
# Register your models here.

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):

    fields = (
        'date_created',
        'user',
        'project',
        'team',
        'logger',
        'message',

    )

    readonly_fields = (
        'date_created',
    )

    list_display = (
        'message',
        'date_created',
        'user',
        'project',
        'team',
        'logger',

    )