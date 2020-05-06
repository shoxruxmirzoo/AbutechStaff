from django.db import models
from shared.models import TimeStampedModel


# Create your models here.
class Team(TimeStampedModel):
    name = models.CharField(max_length=30, null=True)
    task_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Company(TimeStampedModel):
    name = models.CharField(max_length=30, blank=True, null=True)
    posts = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class Staff(TimeStampedModel):
    name = models.CharField(max_length=30, null=True, blank=True)
    telegram_id = models.IntegerField(null=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class TaskType(TimeStampedModel):
    name = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.name)}"


class Admins(TimeStampedModel):
    name = models.ForeignKey(Staff, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.name)}"
