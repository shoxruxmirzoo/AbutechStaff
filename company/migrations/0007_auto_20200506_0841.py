# Generated by Django 3.0.6 on 2020-05-06 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20200506_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='company',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='team',
        ),
    ]