from django.db import models

from company.models import Company, Team, TaskType, Staff, Admins
from shared.models import TimeStampedModel
# Create your models here.


class Tasks(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    is_completed = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    from_admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, blank=True, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    example = models.CharField(max_length=200, blank=True, null=True)
    more = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return f"ID:{self.id} | Team: {self.team} | Type: {self.task_type}"


class CompletedTasks(TimeStampedModel):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.task_id} | Team: {self.team}"
