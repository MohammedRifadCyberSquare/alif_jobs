# Generated by Django 5.1.1 on 2024-09-15 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='staff_status',
            field=models.CharField(default='active', max_length=20),
        ),
    ]
