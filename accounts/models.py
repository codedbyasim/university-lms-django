from django.contrib.auth.models import AbstractUser
from django.db import models
from departments.models import Department, Program # Import Department and Program models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds a 'role' field to categorize users (Admin, Teacher, Student, Department Manager).
    Adds a 'profile_image' field for user avatars.
    Adds 'department' and 'program' fields for departmental organization.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('department_manager', 'Department Manager'), # New role added
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users_in_department')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='users_in_program')


    def is_admin(self):
        """Checks if the user has the 'admin' role."""
        return self.role == 'admin'

    def is_teacher(self):
        """Checks if the user has the 'teacher' role."""
        return self.role == 'teacher'

    def is_student(self):
        """Checks if the user has the 'student' role."""
        return self.role == 'student'
    
    def is_department_manager(self):
        """Checks if the user has the 'department_manager' role."""
        return self.role == 'department_manager'

    def __str__(self):
        return self.username
