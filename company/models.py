from django.db import models
from shared.models import TimeStampedModel


# Create your models here.
class Team(TimeStampedModel):
    name = models.CharField(max_length=30, null=True)
    task_completed = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name


class Company(TimeStampedModel):
    name = models.CharField(max_length=30, blank=True, null=True)
    posts = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Staff(TimeStampedModel):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    telegram_id = models.IntegerField(null=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.first_name)


class TaskType(TimeStampedModel):
    name = models.CharField(max_length=30, null=True, blank=True)
    teamname = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.name)}"


class Admins(TimeStampedModel):
    name = models.ForeignKey(Staff, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.name)}"


class Unknown(TimeStampedModel):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    telegram_id = models.IntegerField(default=0, blank=True, null=True)


class Channel(TimeStampedModel):
    name = models.CharField(max_length=40, blank=True, null=True)
    channel_id = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{str(self.name)}"
