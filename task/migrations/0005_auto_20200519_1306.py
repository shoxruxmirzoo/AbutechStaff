# Generated by Django 3.0.6 on 2020-05-19 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20200518_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedtasks',
            name='company',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='completedtasks',
            name='team',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
