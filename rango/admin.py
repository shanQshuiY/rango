# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rango.models import UserProfile
from rango.models import Category, Page
from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.



class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Page, PageAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

admin.site.register(UserProfile)