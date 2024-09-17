from django.db import models
from django.utils import timezone
 

# Create your models here.

class Admin(models.Model):
    admin_id = models.IntegerField()
    admin_name = models.CharField(max_length = 50)
    last_active = models.DateTimeField(default=timezone.now, null=True)
    password = models.CharField(max_length = 100)

    class Meta:
        db_table = "admin"

class Employee(models.Model):
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 50)
    type = models.CharField(max_length = 100)
    pic = models.ImageField(upload_to = 'employee/')
    password = models.CharField(max_length = 100)
    added_by = models.ForeignKey(Admin, on_delete = models.CASCADE)
    staff_status = models.CharField(max_length = 20, default = 'active')

    class Meta:
        db_table = "staff"


class Job(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 255)
    added_date = models.DateTimeField(default=timezone.now, null=True)
    added_by = models.ForeignKey(Admin, on_delete = models.CASCADE)
    pic = models.ImageField(upload_to = 'job/')
    status = models.CharField(max_length = 100, default = 'pending')

    class Meta:
        db_table = "job"

class JobAssignee(models.Model):
    job = models.ForeignKey(Job, on_delete = models.CASCADE)
    assigned_to = models.ForeignKey(Employee, on_delete = models.CASCADE)
    assigned_date = models.DateTimeField(null=True)
    status = models.CharField(max_length = 100, default = 'pending')
    reason = models.CharField(max_length = 100,)

    class Meta:
        db_table = "job_assignee"

