from django.contrib import admin
from .models import Course, Lecture, Assignment, Enrollment, Submission, Grade # Import new models

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""
    list_display = ('title', 'code', 'teacher', 'created_at')
    list_filter = ('teacher',)
    search_fields = ('title', 'code', 'description')

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    """Admin interface for Lecture model."""
    list_display = ('title', 'course', 'uploaded_by', 'uploaded_at')
    list_filter = ('course', 'uploaded_by')
    search_fields = ('title', 'description')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin interface for Assignment model."""
    list_display = ('title', 'course', 'due_date', 'max_marks', 'uploaded_by')
    list_filter = ('course', 'uploaded_by', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin interface for Enrollment model."""
    list_display = ('student', 'course', 'is_approved', 'enrolled_at')
    list_filter = ('is_approved', 'course')
    search_fields = ('student__username', 'course__title')
    actions = ['approve_selected_enrollments', 'reject_selected_enrollments']

    @admin.action(description='Approve selected enrollments')
    def approve_selected_enrollments(self, request, queryset):
        """Action to approve selected enrollments."""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} enrollments successfully approved.')

    @admin.action(description='Reject selected enrollments')
    def reject_selected_enrollments(self, request, queryset):
        """Action to reject selected enrollments (deletes them)."""
        deleted_count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{deleted_count} enrollments successfully rejected (deleted).', level='warning')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Admin interface for Submission model."""
    list_display = ('assignment', 'student', 'submitted_at', 'status')
    list_filter = ('status', 'assignment__course', 'student')
    search_fields = ('assignment__title', 'student__username', 'text_content')
    raw_id_fields = ('assignment', 'student')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """Admin interface for Grade model."""
    list_display = ('submission', 'marks_obtained', 'graded_by', 'graded_at')
    list_filter = ('graded_by', 'graded_at')
    search_fields = ('submission__assignment__title', 'submission__student__username', 'feedback')
    raw_id_fields = ('submission', 'graded_by')
