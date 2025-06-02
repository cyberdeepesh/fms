# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



from .models import *

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'category', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        

class FranchiseTaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = FranchiseTask
        fields = ['franchise', 'title', 'description', 'due_date', 'priority']
        

class FranchiseStudentForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(FranchiseStudentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:ring focus:outline-none'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class FranchiseStudentProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FranchiseStudentProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['institute'].queryset = Institute.objects.filter(franchise__owner=user)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:ring focus:outline-none'})

    class Meta:
        model = StudentProfile
        fields = ['institute', 'enrollment_number', 'date_of_birth', 'joining_date', 'guardian_name', 'guardian_contact']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }


class FranchiseTeacherForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(FranchiseTeacherForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:ring focus:outline-none'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class FranchiseTeacherProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FranchiseTeacherProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['institute'].queryset = Institute.objects.filter(franchise__owner=user)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:ring focus:outline-none'})

    class Meta:
        model = TeacherProfile
        fields = ['institute', 'expertise_area', 'qualification', 'joining_date']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FranchiseComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category']
        
class SalesReportForm(forms.ModelForm):
    class Meta:
        model = SalesReport
        fields = ['report_file', 'month', 'year', 'total_sales_amount']
        widgets = {
            'month': forms.TextInput(attrs={'placeholder': 'e.g. January'}),
            'year': forms.NumberInput(attrs={'min': 2000}),
            'total_sales_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['course', 'title', 'description', 'due_date']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'status']