# Generated by Django 3.0.6 on 2020-05-07 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_staff_step'),
        ('task', '0005_auto_20200507_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='from_admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Staff'),
        ),
    ]
