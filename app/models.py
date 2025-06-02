from django.db import models
from django.contrib.auth.models import AbstractUser

# Helper Choices
GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

ROLE_CHOICES = (
    ('superadmin', 'Super Admin'),
    ('custom_admin', 'Custom Admin'),
    ('operational_manager', 'Operational Manager'),
    ('franchise_owner', 'Franchise Owner'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('acadamics_head', 'acadamics_head'),
)

COMPLAINT_STATUS = (
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
    ('closed', 'Closed'),
)

COMPLAINT_CATEGORY = (
    ('general', 'General'),
    ('technical', 'Technical'),
    ('administrative', 'Administrative'),
)

ADMISSION_STATUS = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

PAYMENT_STATUS = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed'),
)


class User(AbstractUser):
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    twitter_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Franchise(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'franchise_owner'})
    registration_number = models.CharField(max_length=100, unique=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='franchise_logos/', blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    pincode = models.CharField(max_length=10)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Institute(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='institutes')
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    pincode = models.CharField(max_length=10)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    established_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.franchise.name})"


class Admission(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    applied_course = models.CharField(max_length=255)
    admission_status = models.CharField(max_length=20, choices=ADMISSION_STATUS, default='pending')
    applied_date = models.DateField(auto_now_add=True)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='admission_approved_by')
    approval_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Admission: {self.student.username}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    guardian_name = models.CharField(max_length=255, blank=True, null=True)
    guardian_contact = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    expertise_area = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    joining_date = models.DateField()
    resignation_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role__in': ['teacher', 'acadamics_head']})
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    duration_in_months = models.IntegerField(default=6)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    completion_status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed')], default='in_progress')
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class StudyMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    submission_file = models.FileField(upload_to='task_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.task.title}"


class FeesPayment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - ₹{self.amount}"


class Salary(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.teacher.username} - Salary for {self.month} {self.year}"


class SalesReport(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='sales_reports/')
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    total_sales_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sales Report - {self.franchise.name} ({self.month} {self.year})"


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=COMPLAINT_CATEGORY)
    status = models.CharField(max_length=20, choices=COMPLAINT_STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class FranchiseTask(models.Model):
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'operational_manager'})
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

