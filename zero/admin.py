# -*- coding: utf-8 -*-
from models import *
from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
    list_display = ('verbose_name', 'name','id')
    search_fields = ('verbose_name', 'id')

admin.site.register(Issue, IssueAdmin)

admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Category)
