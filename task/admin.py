from django.contrib import admin
from .models import Tasks, CompletedTasks


# Register your models here.

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'team', 'task_type', 'company', 'deadline', 'from_admin', 'created_at', 'is_completed')


@admin.register(CompletedTasks)
class CompletedTasksAdmin(admin.ModelAdmin):
    list_display = ('completed_id', 'team', 'company', 'time')
