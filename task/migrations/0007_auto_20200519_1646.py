# Generated by Django 3.0.6 on 2020-05-19 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20200519_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='completedtasks',
            old_name='task_id',
            new_name='completed_id',
        ),
    ]