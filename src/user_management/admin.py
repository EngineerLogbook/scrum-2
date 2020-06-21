# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import FieldStudy, TechSkill, Profile, Link


@admin.register(FieldStudy)
class FieldStudyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'date_created',
        'published',
        'reviewed',
    )
    list_filter = ('date_created', 'published', 'reviewed')
    search_fields = ('title',)
    exclude = (
        'slug',
    )


@admin.register(TechSkill)
class TechSkillAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'date_created',
        'published',
        'reviewed',
    )
    list_filter = ('date_created', 'published', 'reviewed')
    search_fields = ('title',)
    exclude = (
        'slug',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date_created',
        'gender',
        # 'bio',
        'degree',
        'is_prof',
        'year_grad',
        # 'token',
        # 'phone',
        'published',
        # 'reviewed',

    )
    list_filter = (
        'date_created',
        'is_prof',
        'field_study',
        'published',
        'reviewed',
    )
    raw_id_fields = ('techskill',)
    exclude = (
        'token',
    )


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'profile')
    list_filter = ('profile',)
    search_fields = ('name',)
