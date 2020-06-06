# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Team, Project


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    fields = (
        'title',
        'description',
        'members',
        'token',
        'reviewed',
    )

    list_display = (

        'title',
        'description',
        'date_created',
        'id',
        'slug',
        'published',
        'reviewed',
        'token',
    )
    list_filter = ('date_created', 'published', 'reviewed')
    raw_id_fields = ('members',)
    search_fields = ('slug',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = (
        'team',
        'title',
        'description',
        'image',
        'logo',
        'access_token',
        'reviewed'

    )

    list_display = (
        'title',
        'team',
        'date_created',
        'slug',

        'access_token',
        'id',

        'image',
        'logo',
        'published',
        'reviewed',
    )
    list_filter = ('date_created', 'published', 'reviewed', 'team')
    search_fields = ('slug',)
