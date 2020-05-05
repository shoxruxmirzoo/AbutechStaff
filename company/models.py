from django.db import models
from shared.models import TimeStampedModel


# Create your models here.
class Team(TimeStampedModel):
    name = models.CharField(max_length=30, null=True)
    task_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Company(TimeStampedModel):
    name = models.CharField(max_length=30, null=True)
    posts = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Staff(TimeStampedModel):
    name = models.CharField(max_length=30, null=True)
    tg_id = models.IntegerField()
    username = models.CharField(max_length=30, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaskType(TimeStampedModel):
    name = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Admins(TimeStampedModel):
    name = models.ForeignKey(Staff, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.name)}"
