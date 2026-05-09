from django import forms
from .models import Course, Lecture, Assignment, Enrollment, Submission, Grade
from accounts.models import User
from departments.models import Department # Import Department model

class CourseForm(forms.ModelForm):
    """
    Form for creating and updating courses.
    Admin/Department Manager can select a teacher for the course within their department.
    """
    # Department field is read-only for Department Managers (auto-filled)
    # Admin can select any department
    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by('name'),
        required=True,
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(role='teacher').order_by('username'), # Initial queryset, will be filtered in view/init
        required=False,
        empty_label="No Teacher Assigned",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'department', 'teacher'] # Added department
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Get the current user from kwargs
        super().__init__(*args, **kwargs)

        if user:
            if user.is_department_manager():
                # For Department Manager, department field is pre-filled and read-only
                self.fields['department'].queryset = Department.objects.filter(pk=user.department.pk)
                self.fields['department'].initial = user.department
                self.fields['department'].widget.attrs['disabled'] = 'disabled'
                
                # Filter teachers to only show those from the manager's department
                self.fields['teacher'].queryset = User.objects.filter(
                    role='teacher', department=user.department
                ).order_by('username')
            elif user.is_admin():
                # For Admin, show all departments and all teachers
                self.fields['department'].queryset = Department.objects.all().order_by('name')
                self.fields['teacher'].queryset = User.objects.filter(role='teacher').order_by('username')
            else:
                # Fallback for other roles (though only admin/manager should create courses)
                self.fields['department'].queryset = Department.objects.none()
                self.fields['teacher'].queryset = User.objects.none()

        # If the form is bound (i.e., submitted with data), and a department is selected,
        # ensure that the teacher queryset includes teachers from that selected department.
        # This is important for form re-rendering after validation errors.
        if self.is_bound and 'department' in self.data:
            try:
                selected_department_id = int(self.data['department'])
                self.fields['teacher'].queryset = User.objects.filter(
                    role='teacher', department_id=selected_department_id
                ).order_by('username')
            except (ValueError, TypeError):
                self.fields['teacher'].queryset = User.objects.none()


class LectureForm(forms.ModelForm):
    """
    Form for uploading lectures.
    """
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'file', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class AssignmentForm(forms.ModelForm):
    """
    Form for creating assignments.
    """
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_marks']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

class EnrollmentForm(forms.ModelForm):
    """
    Form for students to apply for course enrollment.
    """
    class Meta:
        model = Enrollment
        fields = ['course']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

class SubmissionForm(forms.ModelForm):
    """
    Form for students to submit assignments.
    """
    class Meta:
        model = Submission
        fields = ['file', 'text_content']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'text_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class GradeForm(forms.ModelForm):
    """
    Form for teachers/admins to grade submissions.
    """
    class Meta:
        model = Grade
        fields = ['marks_obtained', 'feedback']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
