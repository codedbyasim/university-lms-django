from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('student/', views.student_results, name='student_results'),
    # Removed teacher_submissions as it belongs to the courses app
]
