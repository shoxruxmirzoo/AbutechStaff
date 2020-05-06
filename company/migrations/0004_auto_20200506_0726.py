# Generated by Django 3.0.6 on 2020-05-06 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20200505_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='posts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='company',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='team',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='company.Team'),
        ),
    ]