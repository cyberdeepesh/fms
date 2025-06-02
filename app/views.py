from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm 
from .models import *

def home(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Welcome back {user.username}!")

                    # Role-based redirect
                    if user.role == 'superadmin':
                        return redirect('admin_dashboard')
                    elif user.role == 'custom_admin':
                        return redirect('custom_admin_dashboard')
                    elif user.role == 'student':
                        return redirect('student_dashboard')
                    elif user.role == 'teacher':
                        return redirect('teacher_dashboard')
                    elif user.role == 'operational_manager':
                        return redirect('manager_dashboard')
                    elif user.role == 'franchise_owner':
                        return redirect('franchise_dashboard')
                    else:
                        messages.warning(request, "User has no valid role.")
                        return redirect('home')
                else:
                    messages.error(request, "This account is inactive.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'


from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    # Ensure that the logged-in user is a teacher and get their profile
    teacher_profile = TeacherProfile.objects.get(user=request.user)
    
    # Get the teacher's institute
    institute = teacher_profile.institute
    
    # Get the total number of students in the teacher's institute
    total_students = institute.studentprofile_set.count()

    # Get the total number of tasks assigned by this teacher
    assigned_tasks = Task.objects.filter(assigned_by=request.user)

    # Get the total number of task submissions made for tasks assigned by the teacher
    total_submissions = TaskSubmission.objects.filter(task__assigned_by=request.user).count()

    # Get the teacher's complaints
    complaints = Complaint.objects.filter(user=request.user)

    # Get enrolled students for the teacher's courses, filtering by the teacher's institute
    enrolled_students = CourseEnrollment.objects.filter(course__institute=institute)

    # Get recent task submissions for the teacher's tasks
    recent_submissions = TaskSubmission.objects.filter(task__assigned_by=request.user).order_by('-submitted_at')[:5]

    # Pass the data to the template context
    context = {
        'total_students': total_students,
        'assigned_tasks': assigned_tasks,
        'total_submissions': total_submissions,
        'complaints': complaints,
        'enrolled_students': enrolled_students,
        'recent_submissions': recent_submissions,
    }
    
    return render(request, 'teacher/dashboard.html', context)

def teacher_enrolled_students(request):
    # Get the teacher's profile and institute
    teacher_profile = TeacherProfile.objects.get(user=request.user)
    institute = teacher_profile.institute

    # Get the enrolled students for the teacher's courses at the institute
    enrolled_students = CourseEnrollment.objects.filter(course__institute=institute)

    context = {
        'enrolled_students': enrolled_students,
    }
    return render(request, 'teacher/enrolled_students.html', context)


def teacher_assigned_tasks(request):
    # Fetch the teacher's tasks
    assigned_tasks = Task.objects.filter(assigned_by=request.user)

    context = {
        'assigned_tasks': assigned_tasks,
    }
    return render(request, 'teacher/assigned_tasks.html', context)


def teacher_assign_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            return redirect('assigned_tasks')  # Redirect to the assigned tasks page after saving

    else:
        form = TaskForm()

    return render(request, 'teacher/assign_task.html', {'form': form})

def teacher_my_complaints(request):
    # Fetch complaints created by the teacher
    complaints = Complaint.objects.filter(user=request.user)

    context = {
        'complaints': complaints,
    }
    return render(request, 'teacher/my_complaints.html', context)


def teacher_create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  # Assign the logged-in user as the complaint creator
            complaint.save()
            return redirect('my_complaints')  # Redirect to the complaints page after saving

    else:
        form = ComplaintForm()

    return render(request, 'teacher/create_complaint.html', {'form': form})


@login_required
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")

@login_required
def manager_dashboard(request):
    total_franchises = Franchise.objects.count()
    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    open_complaints = Complaint.objects.filter(status='open').count()

    recent_complaints = Complaint.objects.order_by('-created_at')[:5]
    pending_tasks = FranchiseTask.objects.filter(is_completed=False).order_by('due_date')[:5]

    context = {
        'total_franchises': total_franchises,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'open_complaints': open_complaints,
        'recent_complaints': recent_complaints,
        'pending_tasks': pending_tasks,
    }
    return render(request, "manager/dashboard.html", context)


@login_required
def franchise_list(request):
    franchises = Franchise.objects.select_related("owner").all()
    return render(request, "manager/franchise_list.html", {"franchises": franchises})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "manager/task_list.html", {"tasks": tasks})

@login_required
def complaint_list(request):
    complaints = Complaint.objects.select_related("user").all()
    return render(request, "manager/complaint_list.html", {"complaints": complaints})

@login_required
def complaint_create(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect("complaint_list")
    else:
        form = ComplaintForm()
    return render(request, "manager/complaint_form.html", {"form": form})

@login_required
def complaint_update(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    form = ComplaintForm(request.POST or None, instance=complaint)
    if form.is_valid():
        form.save()
        return redirect("complaint_list")
    return render(request, "manager/complaint_form.html", {"form": form})

@login_required
def complaint_delete(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == "POST":
        complaint.delete()
        return redirect("complaint_list")
    return render(request, "manager/complaint_confirm_delete.html", {"complaint": complaint})


@login_required
def assign_task(request):
    if request.method == 'POST':
        form = FranchiseTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            return redirect('task_list')
    else:
        form = FranchiseTaskForm()
    return render(request, 'manager/assign_task.html', {'form': form})

@login_required
def sales_report_list(request):
    reports = SalesReport.objects.select_related('franchise').all()
    return render(request, 'manager/sales_report_list.html', {'reports': reports})

@login_required
def franchise_dashboard(request):
    franchise = Franchise.objects.get(owner=request.user)
    
    total_students = StudentProfile.objects.filter(institute__franchise=franchise).count()
    total_teachers = TeacherProfile.objects.filter(institute__franchise=franchise).count()
    total_courses = Course.objects.filter(institute__franchise=franchise).count()
    total_admissions = Admission.objects.filter(institute__franchise=franchise).count()

    recent_admissions = Admission.objects.filter(institute__franchise=franchise).order_by('-applied_date')[:5]
    recent_reports = SalesReport.objects.filter(franchise=franchise).order_by('-uploaded_at')[:3]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_admissions': total_admissions,
        'recent_admissions': recent_admissions,
        'recent_reports': recent_reports,
    }
    return render(request, "franchise_owner/dashboard.html", context)


@login_required
def student_list(request):
    students = StudentProfile.objects.filter(institute__franchise__owner=request.user)
    return render(request, "franchise_owner/students.html", {"students": students})

@login_required
def teacher_list(request):
    teachers = TeacherProfile.objects.filter(institute__franchise__owner=request.user)
    return render(request, "franchise_owner/teachers.html", {"teachers": teachers})

@login_required
def course_list(request):
    courses = Course.objects.filter(institute__franchise__owner=request.user)
    return render(request, "franchise_owner/courses.html", {"courses": courses})

@login_required
def franchise_task_list(request):
    tasks = Task.objects.filter(course__institute__franchise__owner=request.user)
    return render(request, "franchise_owner/tasks.html", {"tasks": tasks})

@login_required
def franchise_complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, "franchise_owner/complaints.html", {"complaints": complaints})

@login_required
def franchise_add_student(request):
    if request.method == 'POST':
        user_form = FranchiseStudentForm(request.POST)
        profile_form = FranchiseStudentProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'student'
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('franchise_dashboard')
    else:
        user_form = FranchiseStudentForm()
        profile_form = FranchiseStudentProfileForm()
    return render(request, 'franchise_owner/add_student.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def franchise_add_teacher(request):
    if request.method == 'POST':
        user_form = FranchiseTeacherForm(request.POST)
        profile_form = FranchiseTeacherProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'teacher'
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('franchise_dashboard')
    else:
        user_form = FranchiseTeacherForm()
        profile_form = FranchiseTeacherProfileForm()
    return render(request, 'franchise_owner/add_teacher.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def franchise_add_complaint(request):
    if request.method == 'POST':
        form = FranchiseComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('franchise_dashboard')
    else:
        form = FranchiseComplaintForm()
    return render(request, 'franchise_owner/add_complaint.html', {'form': form})


@login_required
def franchise_upload_report(request):
    franchise = Franchise.objects.get(owner=request.user)
    
    if request.method == 'POST':
        form = SalesReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.franchise = franchise
            report.save()
            return redirect('franchise_report_list')  # Replace with your listing view name
    else:
        form = SalesReportForm()

    return render(request, 'franchise_owner/upload_report.html', {'form': form})

@login_required
def custom_admin_dashboard(request):
    return render(request, "custom_admin/dashboard.html")

from django.db.models import Sum

@login_required
def student_dashboard(request):
    student = request.user

    # Enrolled courses
    enrolled_courses = CourseEnrollment.objects.filter(student=student).select_related('course')

    # Tasks for enrolled courses
    tasks = Task.objects.filter(course__in=[e.course for e in enrolled_courses])

    # Submitted tasks
    submitted_task_ids = TaskSubmission.objects.filter(student=student).values_list('task_id', flat=True)
    pending_tasks = tasks.exclude(id__in=submitted_task_ids)

    # Fees paid and total
    payments = FeesPayment.objects.filter(student=student)
    total_paid = payments.filter(payment_status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    total_due = payments.exclude(payment_status='paid').aggregate(Sum('amount'))['amount__sum'] or 0

    # Complaints
    complaints = Complaint.objects.filter(user=student).order_by('-created_at')

    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'pending_tasks': pending_tasks,
        'total_paid': total_paid,
        'total_due': total_due,
        'complaints': complaints,
    }

    return render(request, 'student/dashboard.html', context)