from django.urls import path
from . import views

app_name = 'alif_admin'

urlpatterns = [
    path('', views.admin_login, name = 'login'),
    path('dashboard', views.admin_dashboard, name = 'dashboard'),
    path('add/staff', views.add_employee, name = 'add_staff'),
    path('add/job', views.add_job, name = 'add_job'),
    path('job/pending', views.pending_jobs, name = 'pending_jobs'),
    path('job/history', views.job_history, name = 'job_history'),
    path('job/rejected/list', views.load_rejected_jobs, name = 'rejected_jobs'),
    path('staff/active/list', views.load_active_staff, name = 'active_staff'),

]