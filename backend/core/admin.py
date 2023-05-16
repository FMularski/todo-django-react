from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Task


class TaskAdmin(ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
