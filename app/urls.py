from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/assigned_tasks/', views.teacher_assigned_tasks, name='teacher_assigned_tasks'),
    path('teacher/enrolled_students/', views.teacher_enrolled_students, name='teacher_enrolled_students'),
    path('teacher/my_complaints/', views.teacher_my_complaints, name='teacher_my_complaints'),
    path('teacher/create_complaint/', views.teacher_create_complaint, name='teacher_create_complaint'),
    path('teacher/assign_task/', views.teacher_assign_task, name='teacher_assign_task'),
    path('dashboard/custom_admin/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('franchises/', views.franchise_list, name='franchise_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/assign/', views.assign_task, name='assign_task'),
    path('sales-reports/', views.sales_report_list, name='sales_report_list'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/create/', views.complaint_create, name='complaint_create'),
    path('complaints/update/<int:pk>/', views.complaint_update, name='complaint_update'),
    path('complaints/delete/<int:pk>/', views.complaint_delete, name='complaint_delete'),
    path('dashboard/franchise/', views.franchise_dashboard, name='franchise_dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('courses/', views.course_list, name='course_list'),
    path('mytasks/', views.franchise_task_list, name='franchise_task_list'),
    path('mycomplaints/', views.franchise_complaint_list, name='franchise_complaint_list'),
    path('franchise/students/add/', views.franchise_add_student, name='franchise_add_student'),
    path('franchise/teachers/add/', views.franchise_add_teacher, name='franchise_add_teacher'),
    path('franchise/complaints/add/', views.franchise_add_complaint, name='franchise_add_complaint'),
    path('franchise/upload-report/', views.franchise_upload_report, name='franchise_upload_report'),


    
    
]
