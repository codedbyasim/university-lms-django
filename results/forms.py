from django import forms
from .models import Grade # Only import Grade, as Submission is no longer in results/models.py

class GradeForm(forms.ModelForm):
    """
    Form for teachers/admins to grade submissions within the results context.
    """
    class Meta:
        model = Grade
        fields = ['marks_obtained', 'feedback']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Removed SubmissionForm as the Submission model is no longer in results/models.py
