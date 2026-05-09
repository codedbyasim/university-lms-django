from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('change_password/', views.change_password_view, name='change_password'),
    # Admin-specific URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create_user/', views.admin_create_user, name='admin_create_user'),
    path('get_programs_by_department/', views.get_programs_by_department, name='get_programs_by_department'),
    # Department Manager-specific URLs
    path('department_manager/dashboard/', views.department_manager_dashboard, name='department_manager_dashboard'), # New URL
    # Teacher-specific URLs
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    # Student-specific URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    # Removed signup URL as per instruction
]