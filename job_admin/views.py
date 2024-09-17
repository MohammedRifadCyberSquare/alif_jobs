from django.shortcuts import render, redirect
from .models import *
from employee.models import *
from django.utils import timezone

from django.db.models import Q
from django.db.models import OuterRef, Subquery


def admin_login(request):
    message = ''
    if request.method == 'POST':
        admin_id = request.POST['adminId']
        password = request.POST['password']

        user = Admin.objects.filter(admin_id=admin_id, password=password)

        if user:
            request.session['admin_id'] = user[0].id
            request.session['admin_name'] = user[0].admin_name
            print('hhh')
            return redirect('alif_admin:dashboard')

        else:
            print('here')
            message = 'User Name or Password Incorrect'
    return render(request, 'job_admin/login.html', {'message': message})


def admin_dashboard(request):
    return render(request, 'job_admin/dashboard.html')


def add_employee(request):
    message = ''

    if request.method == 'POST':
        emp_id = request.POST['empId']
        emp_name = request.POST['empName']
        emp_phone = request.POST['empPhone']
        emp_type = request.POST['empType']

        if request.FILES:
            emp_pic = request.FILES['empPic']
        else:
            pass

        employee = Employee.objects.filter(emp_id=emp_id)

        if not employee:
            _ = Employee(emp_id=emp_id, emp_name=emp_name,
                         type=emp_type,
                         phone=emp_phone,
                         pic=emp_pic,
                         password='alif@12345',
                         added_by_id = request.session['admin_id']
                         ).save()
            message = 'Staff Added Succesfully '

        else:
            message = 'Staff ID Exist'

    return render(request, 'job_admin/add_employee.html', {'message': message})


def add_job(request):
    staffs = Employee.objects.all().values('id', 'emp_name')
    message = ''

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        staff = request.POST['staff']


        if request.FILES:
            pic = request.FILES['pic']
        else:
            pass

        job = Job(title=title, description=description,
                added_by=Admin.objects.get(id=request.session['admin_id']),
                pic = pic
                )
        job.save()
        assignee = JobAssignee(job_id = job.id, assigned_to_id =  staff,
                    assigned_date = timezone.now(),)
        assignee.save()

        message = 'Job Added Succesfully '

    return render(request, 'job_admin/add_job.html', {'staffs': staffs, 'message': message})


def pending_jobs(request):
    latest_assignee = JobAssignee.objects.filter(job=OuterRef('pk')).order_by('-assigned_date')
    jobs = Job.objects.annotate(
        current_assignee=Subquery(latest_assignee.values('assigned_to__emp_name')[:1]),
        current_assignee_status=Subquery(latest_assignee.values('status')[:1])
    ).filter(current_assignee_status='pending') 
    
    context = {
        'jobs': jobs
    }
    return render(request, 'job_admin/pending_jobs.html', {'jobs': jobs,})

def job_history(request):

    jobs = JobAssignee.objects.filter(Q(status = 'completed') | Q(status = 'cancelled'))
    context = {
        'jobs': jobs
    }
    return render(request, 'job_admin/job_history.html', {'jobs': jobs,})

def load_active_staff(request):

    staffs = Employee.objects.filter(staff_status = 'active')
    context = {
        'staffs': staffs
    }
    return render(request, 'job_admin/active_staff_list.html', {'staffs': staffs,})

def load_rejected_jobs(request):
    

    jobs = JobAssignee.objects.filter( status = 'rejected')
    print(jobs)
    staffs = Employee.objects.all().values('id', 'emp_name')
    if request.method == 'POST':
        job_id = request.POST['job_id']
        assign_id = request.POST['assign_id']
        re_assigned_staff = request.POST['staff_assigned']


        JobAssignee.objects.filter(id = assign_id).update(status = 're assigned')
        _ = JobAssignee(
            job_id = job_id,
            assigned_to_id = re_assigned_staff,
            assigned_date  = timezone.now(),

        ).save()
        
        return redirect('alif_admin:rejected_jobs')
    return render(request, 'job_admin/rejected_jobs.html', {'jobs': jobs, 'staffs': staffs})
