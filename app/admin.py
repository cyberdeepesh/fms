from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_active', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'registration_number', 'phone', 'email', 'is_active')
    search_fields = ('name', 'owner__username', 'registration_number')
    list_filter = ('is_active', 'city', 'state')


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'franchise', 'city', 'state', 'phone', 'is_active')
    search_fields = ('name', 'franchise__name')
    list_filter = ('city', 'state', 'is_active')


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'institute', 'applied_course', 'admission_status', 'applied_date')
    search_fields = ('student__username', 'applied_course')
    list_filter = ('admission_status', 'applied_date')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'institute', 'enrollment_number', 'joining_date', 'is_active')
    search_fields = ('user__username', 'enrollment_number')
    list_filter = ('is_active', 'joining_date')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'institute', 'expertise_area', 'joining_date', 'is_active')
    search_fields = ('user__username', 'expertise_area')
    list_filter = ('is_active', 'joining_date')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'institute', 'duration_in_months', 'fee', 'is_active', 'created_at')
    search_fields = ('title', 'institute__name')
    list_filter = ('is_active', 'created_at')


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'uploaded_at')
    search_fields = ('title', 'course__title')
    list_filter = ('uploaded_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'assigned_by', 'due_date', 'assigned_at')
    search_fields = ('title', 'assigned_by__username')
    list_filter = ('due_date',)


@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'student', 'submitted_at')
    search_fields = ('task__title', 'student__username')
    list_filter = ('submitted_at',)


@admin.register(FeesPayment)
class FeesPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'institute', 'amount', 'payment_status', 'payment_date')
    search_fields = ('student__username', 'institute__name')
    list_filter = ('payment_status', 'payment_date')


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'institute', 'amount', 'month', 'year', 'payment_status', 'payment_date')
    search_fields = ('teacher__username', 'month', 'year')
    list_filter = ('payment_status', 'month', 'year')


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'franchise', 'month', 'year', 'total_sales_amount', 'uploaded_at')
    search_fields = ('franchise__name', 'month', 'year')
    list_filter = ('month', 'year')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'category', 'status', 'created_at')
    search_fields = ('user__username', 'title')
    list_filter = ('status', 'category', 'created_at')


@admin.register(FranchiseTask)
class FranchiseTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'franchise', 'assigned_by', 'due_date', 'priority', 'is_completed')
    search_fields = ('title', 'franchise__name', 'assigned_by__username')
    list_filter = ('priority', 'is_completed', 'due_date')

admin.site.register(CourseEnrollment)