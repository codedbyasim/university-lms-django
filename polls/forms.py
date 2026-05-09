from django import forms
from .models import Poll, Choice

class PollForm(forms.ModelForm):
    """
    Form for creating a new poll.
    """
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text="Optional: Set an end date for the poll."
    )

    class Meta:
        model = Poll
        fields = ['question', 'is_active', 'end_date']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ChoiceForm(forms.ModelForm):
    """
    Form for adding choices to a poll.
    Used in a formset for multiple choices.
    """
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formset for managing multiple choices for a poll
ChoiceFormSet = forms.inlineformset_factory(
    Poll,
    Choice,
    form=ChoiceForm,
    extra=2, # Start with 2 empty choice fields
    can_delete=True,
    min_num=2, # Require at least 2 choices
    validate_min=True
)
