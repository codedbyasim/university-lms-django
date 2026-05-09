from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q # Import Q for complex queries
from django.utils import timezone # Import timezone for date comparisons

from accounts.views import is_admin, is_teacher, is_student # Import custom test functions
from accounts.forms import UserProfileForm # Used in profile view
from accounts.models import User # Import User model for choices in forms

from .models import Course, Lecture, Assignment, Enrollment, Submission, Grade # Added Submission, Grade
from .forms import CourseForm, LectureForm, AssignmentForm, EnrollmentForm, SubmissionForm, GradeForm # Added SubmissionForm, GradeForm

# --- Admin Views (Existing) ---
@login_required
@user_passes_test(is_admin)
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            # Assuming admin is creating, but teacher is assigned via form
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('manage_courses')
        else:
            messages.error(request, 'Error creating course. Please check the form.')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def manage_courses(request):
    courses = Course.objects.all().order_by('code')
    return render(request, 'courses/manage_courses.html', {'courses': courses})

@login_required
@user_passes_test(is_admin)
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('manage_courses')
        else:
            messages.error(request, 'Error updating course. Please check the form.')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
@user_passes_test(is_admin)
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('manage_courses')
    return render(request, 'courses/delete_course_confirm.html', {'course': course}) # You might need to create this template

@login_required
@user_passes_test(is_admin)
def approve_enrollment(request):
    pending_enrollments = Enrollment.objects.filter(is_approved=False).order_by('enrolled_at')
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        action = request.POST.get('action')
        enrollment = get_object_or_404(Enrollment, pk=enrollment_id)

        if action == 'approve':
            enrollment.is_approved = True
            enrollment.save()
            messages.success(request, f"Enrollment for {enrollment.student.username} in {enrollment.course.code} approved.")
        elif action == 'reject':
            enrollment.delete() # Or set a status like is_rejected=True
            messages.warning(request, f"Enrollment for {enrollment.student.username} in {enrollment.course.code} rejected.")
        return redirect('approve_enrollment')
    return render(request, 'courses/approve_enrollment.html', {'pending_enrollments': pending_enrollments})


# --- Teacher Views ---
@login_required
@user_passes_test(is_teacher)
def teacher_courses(request):
    """
    Lists courses assigned to the logged-in teacher.
    Annotates each course with the count of approved students.
    """
    courses = Course.objects.filter(teacher=request.user).annotate(
        approved_students_count=Count('enrollments', filter=Q(enrollments__is_approved=True))
    ).order_by('title')
    return render(request, 'courses/teacher_courses.html', {'courses': courses})

@login_required
@user_passes_test(is_teacher)
def teacher_course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    lectures = course.lectures.all().order_by('-uploaded_at')
    assignments = course.assignments.all().order_by('-due_date')

    if request.method == 'POST':
        if 'upload_lecture' in request.POST:
            lecture_form = LectureForm(request.POST, request.FILES)
            if lecture_form.is_valid():
                lecture = lecture_form.save(commit=False)
                lecture.course = course
                lecture.uploaded_by = request.user
                lecture.save()
                messages.success(request, 'Lecture uploaded successfully!')
                return redirect('teacher_course_detail', pk=pk)
            else:
                messages.error(request, 'Error uploading lecture. Please check the form.')
        elif 'create_assignment' in request.POST:
            assignment_form = AssignmentForm(request.POST)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.course = course
                assignment.uploaded_by = request.user
                assignment.save()
                messages.success(request, 'Assignment created successfully!')
                return redirect('teacher_course_detail', pk=pk)
            else:
                messages.error(request, 'Error creating assignment. Please check the form.')
    else:
        lecture_form = LectureForm()
        assignment_form = AssignmentForm()

    return render(request, 'courses/teacher_course_detail.html', {
        'course': course,
        'lectures': lectures,
        'assignments': assignments,
        'lecture_form': lecture_form,
        'assignment_form': assignment_form
    })

@login_required
@user_passes_test(is_teacher)
def view_enrolled_students(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, teacher=request.user)
    enrolled_students = Enrollment.objects.filter(course=course, is_approved=True).order_by('student__username')
    return render(request, 'courses/view_enrolled_students.html', {
        'course': course,
        'enrolled_students': enrolled_students
    })

@login_required
@user_passes_test(is_teacher)
def view_assignment_submissions(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk, course__teacher=request.user)
    # Fetch submissions and prefetch related grades if they exist
    submissions = Submission.objects.filter(assignment=assignment).select_related('student', 'grade').order_by('-submitted_at')
    
    return render(request, 'courses/view_assignment_submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })

@login_required
@user_passes_test(is_teacher)
def grade_submission(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk, assignment__course__teacher=request.user)
    
    # Try to get existing grade or create a new one
    grade, created = Grade.objects.get_or_create(submission=submission, defaults={'marks_obtained': 0})

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.graded_by = request.user # Set the grader to the current teacher
            grade.graded_at = timezone.now()
            grade.save()
            
            # Update submission status to 'graded'
            submission.status = 'graded'
            submission.save()

            messages.success(request, f"Submission for {submission.student.username} graded successfully!")
            return redirect('view_assignment_submissions', assignment_pk=submission.assignment.pk)
        else:
            messages.error(request, 'Error grading submission. Please check the form.')
    else:
        form = GradeForm(instance=grade)
            
    return render(request, 'courses/grade_submission.html', {
        'submission': submission,
        'form': form
    })

@login_required
@user_passes_test(is_teacher)
def teacher_submissions_overview(request):
    """
    Teacher view to list all assignments they are responsible for,
    along with a count of submissions for each.
    """
    assignments = Assignment.objects.filter(uploaded_by=request.user).annotate(
        submission_count=Count('course_submissions') # Corrected related_name
    ).order_by('-due_date')
    
    return render(request, 'courses/teacher_submissions_overview.html', {'assignments': assignments})


# --- Student Views ---
@login_required
@user_passes_test(is_student)
def apply_for_enrollment(request):
    # Get courses the student is not already enrolled in (approved or not)
    enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course__id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids).order_by('title')

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.save()
            messages.success(request, f"Enrollment request for {enrollment.course.title} submitted. Awaiting admin approval.")
            return redirect('student_courses') # Redirect to my courses, where they'll see pending status
        else:
            messages.error(request, 'Error submitting enrollment request. Please check the form.')
    else:
        form = EnrollmentForm()
        # Dynamically set queryset for the course field to show only available courses
        form.fields['course'].queryset = available_courses
    return render(request, 'courses/apply_enrollment.html', {'form': form, 'available_courses': available_courses})

@login_required
@user_passes_test(is_student)
def student_courses(request):
    # Only show courses where enrollment is approved
    enrollments = Enrollment.objects.filter(student=request.user, is_approved=True).select_related('course').order_by('course__title')
    courses = [enrollment.course for enrollment in enrollments]
    return render(request, 'courses/student_courses.html', {'courses': courses})

@login_required
@user_passes_test(is_student)
def student_course_detail(request, pk):
    # Ensure the student is approved for this course
    enrollment = get_object_or_404(Enrollment, student=request.user, course__pk=pk, is_approved=True)
    course = enrollment.course
    
    lectures = course.lectures.all().order_by('-uploaded_at')
    assignments = course.assignments.all().order_by('-due_date')

    # Add submission status to assignments for display
    for assignment in assignments:
        submission_exists = Submission.objects.filter(student=request.user, assignment=assignment).exists()
        assignment.has_submitted = submission_exists

    return render(request, 'courses/student_course_detail.html', {
        'course': course,
        'lectures': lectures,
        'assignments': assignments
    })

@login_required
@user_passes_test(is_student)
def submit_assignment(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    
    # Ensure student is enrolled and approved for this course
    if not Enrollment.objects.filter(student=request.user, course=assignment.course, is_approved=True).exists():
        messages.error(request, "You are not enrolled in this course or your enrollment is not approved.")
        return redirect('student_course_detail', pk=assignment.course.pk)

    # Get existing submission if any, otherwise create new
    existing_submission = Submission.objects.filter(student=request.user, assignment=assignment).first()

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=existing_submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.status = 'submitted' # Set status to submitted
            submission.submitted_at = timezone.now() # Update submission time
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('student_course_detail', pk=assignment.course.pk)
        else:
            messages.error(request, 'Error submitting assignment. Please check the form.')
    else:
        form = SubmissionForm(instance=existing_submission)
            
    return render(request, 'courses/submit_assignment.html', {
        'assignment': assignment,
        'form': form,
        'existing_submission': existing_submission
    })

# --- Notifications Views (Existing) ---
# Assuming these are in a separate 'notifications' app or integrated here
# Note: Notification model and forms are assumed to be defined in the notifications app.
# If not, you'll need to create them.
# from notifications.models import Notification
# from notifications.forms import NotificationForm

# @login_required
# def notifications_list(request):
#     user = request.user
#     if user.is_admin():
#         notifications = Notification.objects.filter(Q(target_roles='all') | Q(target_roles='admins'), is_active=True).order_by('-created_at')
#     elif user.is_teacher():
#         notifications = Notification.objects.filter(Q(target_roles='all') | Q(target_roles='teachers'), is_active=True).order_by('-created_at')
#     elif user.is_student():
#         notifications = Notification.objects.filter(Q(target_roles='all') | Q(target_roles='students'), is_active=True).order_by('-created_at')
#     else:
#         notifications = Notification.objects.none() # No notifications for unassigned roles

#     return render(request, 'notifications/notifications_list.html', {'notifications': user_notifications})

# @login_required
# @user_passes_test(is_admin)
# def create_notification(request):
#     if request.method == 'POST':
#         form = NotificationForm(request.POST)
#         if form.is_valid():
#             notification = form.save(commit=False)
#             notification.created_by = request.user
#             notification.save()
#             messages.success(request, 'Notification created successfully!')
#             return redirect('notifications_list')
#         else:
#             messages.error(request, 'Error creating notification. Please check the form.')
#     else:
#         form = NotificationForm()
#     return render(request, 'notifications/create_notification.html', {'form': form})
