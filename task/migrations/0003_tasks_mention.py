# Generated by Django 3.0.6 on 2020-05-18 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20200518_1135'),
        ('task', '0002_auto_20200518_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='mention',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Staff'),
        ),
    ]