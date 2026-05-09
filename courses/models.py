from django.db import models
from accounts.models import User # Import your custom User model
from departments.models import Department, Program # Import Department and Program models

class Course(models.Model):
    """
    Represents a course in the LMS.
    Can be assigned to a teacher and belongs to a specific department.
    """
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                limit_choices_to={'role': 'teacher'}, related_name='assigned_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}: {self.title}"

class Lecture(models.Model):
    """
    Represents a lecture within a course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='lectures/', blank=True, null=True) # For lecture materials (PDFs, PPTs)
    video_url = models.URLField(blank=True, null=True) # For embedded video lectures
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']})
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lecture: {self.title} ({self.course.code})"

class Assignment(models.Model):
    """
    Represents an assignment for a course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']})
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assignment: {self.title} ({self.course.code})"

class Enrollment(models.Model):
    """
    Represents a student's enrollment in a course.
    Requires admin approval.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    is_approved = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') # A student can enroll in a course only once

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.code} (Approved: {self.is_approved})"

class Submission(models.Model):
    """
    Represents a student's submission for an assignment.
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='course_submissions') # Added related_name
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='submissions')
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    # Status can be 'submitted', 'graded', 'late', etc.
    status = models.CharField(max_length=50, default='submitted')

    class Meta:
        unique_together = ('assignment', 'student') # A student can submit only once per assignment

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.title}"

class Grade(models.Model):
    """
    Represents a grade given to a submission.
    """
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'role__in': ['admin', 'teacher']}, related_name='courses_grades') # Added related_name
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade for {self.submission.student.username}'s {self.submission.assignment.title}: {self.marks_obtained}"
