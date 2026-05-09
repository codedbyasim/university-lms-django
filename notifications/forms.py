from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    """
    Form for creating new notifications/announcements.
    """
    class Meta:
        model = Notification
        fields = ['title', 'message', 'target_roles', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'target_roles': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
