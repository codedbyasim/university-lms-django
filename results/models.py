from django.db import models
from accounts.models import User
# Import Submission from courses app directly, as it's the primary submission record
from courses.models import Submission as CourseSubmission, Assignment 

# The previous Submission model in results app was redundant and causing clashes.
# We will now directly use the Submission model from the courses app for results.

class Grade(models.Model):
    """
    Represents a grade recorded in the results app.
    This model now directly links to the Submission model from the courses app.
    """
    submission = models.OneToOneField(CourseSubmission, on_delete=models.CASCADE, related_name='results_grade')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) # Added default=0.0
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'role__in': ['admin', 'teacher']}, related_name='results_grades')
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result Grade for {self.submission.student.username}'s {self.submission.assignment.title}: {self.marks_obtained}"

