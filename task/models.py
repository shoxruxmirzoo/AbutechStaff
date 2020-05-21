from django.db import models

from company.models import Company, Team, TaskType, Staff, Admins
from shared.models import TimeStampedModel
# Create your models here.


class Tasks(TimeStampedModel):
    task_id = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False, blank=True)
    company = models.CharField(max_length=40, blank=True, null=True)
    team = models.CharField(max_length=50, blank=True, null=True)
    from_admin = models.CharField(max_length=30, blank=True, null=True)
    task_type = models.CharField(max_length=1024, blank=True, null=True)
    deadline = models.CharField(max_length=30, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    more = models.CharField(max_length=1024, blank=True, null=True)
    mention = models.CharField(max_length=40, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"ID:{self.task_id} | Team: {self.team} | Type: {self.company}"


class CompletedTasks(TimeStampedModel):
    completed_id = models.IntegerField(default=0)
    team = models.CharField(max_length=40, null=True, blank=True)
    company = models.CharField(max_length=40, null=True, blank=True)
    time = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.completed_id} | Team: {self.team}"

