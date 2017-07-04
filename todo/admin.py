from django.contrib import admin

from todo.models import Task


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ['text', 'done', 'user', 'created', 'updated']


admin.site.register(Task, TaskAdmin)
