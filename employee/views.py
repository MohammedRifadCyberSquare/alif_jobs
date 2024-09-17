from django.shortcuts import render,redirect
from .models import *
from job_admin.models import Employee
from job_admin.models import JobAssignee,Job
from django.db.models import Q

 
def staff_login(request):
    message = ''
    if request.method == 'POST':
        staff_id = request.POST['staffId']
        password = request.POST['password']

        user = Employee.objects.filter(emp_id = staff_id, password=password)
        print('*************')
        if user:
            request.session['staff_id'] = user[0].id
            request.session['staff_name'] = user[0].emp_name
            return redirect('staff:dashboard')

        else:
            print('here')
            message = 'User Name or Password Incorrect'
    return render(request, 'employee/login.html', {'message': message})


def staff_dashboard(request):
    jobs = JobAssignee.objects.filter(Q(status = 'pending') | Q(status = 'cancel'), assigned_to_id = request.session['staff_id'])
    print(jobs, request.session['staff_id'])
    return render(request, 'employee/pending_jobs.html', {'jobs': jobs})
    # return render(request, 'employee/dashboard.html')

def pending_jobs(request):
    jobs = JobAssignee.objects.filter(Q(status = 'pending') | Q(status = 'cancel'), assigned_to_id = request.session['staff_id'])
    print(jobs)
    return render(request, 'employee/pending_jobs.html', {'jobs': jobs})

def reject_reason(request, assign_id):
    if request.method == 'POST':
        reason = request.POST['reason']
        record = JobAssignee.objects.get(id = assign_id)
        record.reason = reason
        record.status = 'rejected'
        record.save()
        return redirect('staff:dashboard')
    return render(request, 'employee/reject_reason.html')


def update_job_completed(request, assign_id):
    job_assign_record = JobAssignee.objects.get(id = assign_id)
    job_assign_record.status = 'completed'
    job_assign_record.save()
    job_id = job_assign_record.job.id
    print(job_assign_record.job.id)
    job_record = Job.objects.get(id = job_id)
    job_record.status = 'completed'
    print(job_record.id,'*********')
    job_record.save()
    return redirect('staff:pending_jobs')
