from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User
from departments.models import Department, Program # Import Department and Program

class AdminUserCreationForm(UserCreationForm):
    """
    Form for Admin users to create new user accounts.
    Includes the 'role', 'department', and 'program' fields for new users.
    """
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by('name'), # Ensure all departments are loaded here
        required=False,
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # Reverted program to ModelChoiceField. Its options will be populated by JavaScript via AJAX.
    program = forms.ModelChoiceField(
        queryset=Program.objects.none(), # Initially no programs, will be populated by JS
        required=False,
        empty_label="Select Program",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'department', 'program',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure department queryset is set
        self.fields['department'].queryset = Department.objects.all().order_by('name')

        # If the form is pre-populated (e.g., on edit or error reload)
        # then set the initial queryset for the program field.
        # Otherwise, it remains Program.objects.none() and AJAX populates it.
        if self.instance and self.instance.department:
            self.fields['program'].queryset = Program.objects.filter(department=self.instance.department).order_by('name')
        elif self.is_bound and 'department' in self.data:
            try:
                department_id = int(self.data['department'])
                self.fields['program'].queryset = Program.objects.filter(department_id=department_id).order_by('name')
            except (ValueError, TypeError):
                # Handle cases where department_id might be invalid
                self.fields['program'].queryset = Program.objects.none()
        else:
            self.fields['program'].queryset = Program.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        department = cleaned_data.get('department')
        program = cleaned_data.get('program') # This will now be a Program instance if valid

        # Require department for Teachers, Students, and Department Managers
        if role in ['teacher', 'student', 'department_manager']:
            if not department:
                self.add_error('department', "Department is required for Teachers, Students, and Department Managers.")
            # Program is not strictly required for Department Managers, but it is for Teachers and Students
            if role in ['teacher', 'student'] and not program:
                self.add_error('program', "Program is required for Teachers and Students.")
        elif role == 'admin':
            # For admin, department and program should not be set
            if department:
                self.add_error('department', "Admin users should not be assigned to a department.")
            if program:
                self.add_error('program', "Admin users should not be assigned to a program.")
        
        # Ensure program belongs to the selected department if a program is selected
        if department and program and program.department != department:
            self.add_error('program', "Selected program does not belong to the selected department.")

        return cleaned_data


class LoginForm(AuthenticationForm):
    """
    Standard Django authentication form for user login.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserProfileForm(forms.ModelForm):
    """
    Form for users to edit their profile details.
    Includes department and program for display, but often these are not editable by user.
    """
    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by('name'),
        required=False,
        empty_label="No Department",
        widget=forms.Select(attrs={'class': 'form-control'}),
        disabled=True # Usually not editable by user
    )
    program = forms.ModelChoiceField(
        queryset=Program.objects.all().order_by('name'),
        required=False,
        empty_label="No Program",
        widget=forms.Select(attrs={'class': 'form-control'}),
        disabled=True # Usually not editable by user
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', 'program'] # Added department and program
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
