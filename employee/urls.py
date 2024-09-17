from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.staff_login, name = 'login'),
    path('dashboard', views.staff_dashboard, name = 'dashboard'),
    path('pending/jobs', views.pending_jobs, name = 'pending_jobs'),
    path('pending/jobs/reject/<int:assign_id>', views.reject_reason, name = 'reject_reason'),
    path('pending/jobs/completed/<int:assign_id>', views.update_job_completed, name = 'update_job_completed'),

    # path('add/employee', views.add_employee, name = 'add_employee'),
    # path('add/job', views.add_job, name = 'add_job'),
    # path('job/pending', views.pending_jobs, name = 'pending_jobs'),
    # path('job/history', views.job_history, name = 'job_history'),
]