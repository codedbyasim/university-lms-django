from django.contrib import admin
from .models import Grade # Only import Grade, as Submission is removed

# Unregister Submission if it was previously registered
# from .models import Submission # If you had this, remove it

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """Admin interface for Grade model."""
    list_display = ('submission', 'marks_obtained', 'graded_by', 'graded_at')
    list_filter = ('graded_by', 'graded_at')
    search_fields = ('submission__assignment__title', 'submission__student__username', 'feedback')
    raw_id_fields = ('submission', 'graded_by')
