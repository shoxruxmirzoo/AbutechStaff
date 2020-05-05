from django.contrib import admin
from .models import Tasks, CompletedTasks


# Register your models here.

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'task_type', 'company', 'deadline', 'from_admin', 'is_completed')


@admin.register(CompletedTasks)
class CompletedTasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'company', 'time')
