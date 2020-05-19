from django.contrib import admin
from .models import Team, TaskType, Company, Staff, Admins, Unknown, Channel


# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_completed')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'posts')


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'teamname')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'team', 'username',  'telegram_id')


@admin.register(Admins)
class AdminsAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')


@admin.register(Unknown)
class UnknownAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'username', 'telegram_id')

@admin.register(Channel)
class UnknownAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel_id')
