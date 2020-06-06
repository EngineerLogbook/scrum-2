# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Logger, LogFile, LogURL


class LogFileInLine(admin.TabularInline):
    model = LogFile
    fields = (
        'title',
        'file',
        'filetype',

    )
    extra = 1
    verbose_name = "Attachment"


class LogURLInline(admin.TabularInline):
    model = LogURL
    fields = (
        'url',
        'id',
    )
    extra = 1
    verbose_name = "URL"


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    fields = (
        'title', 'note', 'user', 'project', 'reviewed'
    )
    list_display = (
        'title',
        'project',
        'user',
        'date_created',
        'date_modified',
        'slug',
        'published',
        'reviewed',
        'id',
        # 'note',
    )
    list_filter = (
        'date_created',
        'published',
        'reviewed',
        'date_modified',
        'project',
    )
    search_fields = ('slug',)
    inlines = [LogFileInLine, LogURLInline]


@admin.register(LogFile)
class LogFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'date_created',
        'published',
        'reviewed',
        'file',
        'filetype',
    )
    list_filter = ('date_created', 'published', 'reviewed', )
    search_fields = ('slug',)


@admin.register(LogURL)
class LogURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'log')
    list_filter = ('log',)
