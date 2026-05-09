from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages

# Import the Submission model from the courses app, as it's the primary source
from courses.models import Submission as CourseSubmission, Assignment
from accounts.views import is_student, is_teacher, is_admin # Import role test functions
from .models import Grade # Import the Grade model from results app
from .forms import GradeForm # Import GradeForm from results app

@login_required
@user_passes_test(is_student)
def student_results(request):
    """
    Student view to see their grades for all their submissions.
    """
    # Get all grades for the logged-in student's submissions
    # Filter for submissions made by the current student
    # Use select_related to efficiently fetch related submission and assignment data
    student_submissions_with_grades = CourseSubmission.objects.filter(
        student=request.user,
        grade__isnull=False # Only show submissions that have been graded
    ).select_related('assignment', 'assignment__course', 'grade').order_by('-submitted_at')

    context = {
        'student_submissions_with_grades': student_submissions_with_grades
    }
    return render(request, 'results/student_results.html', context)

# You might also have a view for teachers to see grades for their courses
# or for admins to manage all grades.
# Example (if needed, this would be in courses/views.py or a new results/views.py for teachers/admins)
# @login_required
# @user_passes_test(is_teacher)
# def teacher_grades_overview(request):
#     # Logic for teachers to see grades for assignments in their courses
#     pass

# @login_required
# @user_passes_test(is_admin)
# def admin_grades_management(request):
#     # Logic for admins to manage all grades
#     pass
