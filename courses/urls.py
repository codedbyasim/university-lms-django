from django.urls import path
from . import views

urlpatterns = [
    # Admin URLs
    path('admin/create/', views.create_course, name='create_course'),
    path('admin/manage/', views.manage_courses, name='manage_courses'),
    path('admin/edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('admin/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('admin/enrollments/approve/', views.approve_enrollment, name='approve_enrollment'),

    # Teacher URLs
    path('teacher/my_courses/', views.teacher_courses, name='teacher_courses'),
    path('teacher/course/<int:pk>/', views.teacher_course_detail, name='teacher_course_detail'),
    path('teacher/course/<int:course_pk>/students/', views.view_enrolled_students, name='view_enrolled_students'),
    path('teacher/assignment/<int:assignment_pk>/submissions/', views.view_assignment_submissions, name='view_assignment_submissions'),
    path('teacher/submissions/', views.teacher_submissions_overview, name='teacher_submissions'), # General submissions overview
    path('teacher/submissions/<int:submission_pk>/grade/', views.grade_submission, name='grade_submission'), # New: Grade submission URL

    # Student URLs
    path('student/apply_enrollment/', views.apply_for_enrollment, name='apply_enrollment'),
    path('student/my_courses/', views.student_courses, name='student_courses'),
    path('student/course/<int:pk>/', views.student_course_detail, name='student_course_detail'),
    path('student/assignment/<int:assignment_pk>/submit/', views.submit_assignment, name='submit_assignment'),
]
