from django.db import models
from accounts.models import User

class Notification(models.Model):
    """
    Represents a system-wide notification or announcement.
    Can be targeted to specific roles or all users.
    """
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    created_at = models.DateTimeField(auto_now_add=True)
    # Target audience
    target_roles = models.CharField(
        max_length=50,
        choices=(
            ('all', 'All Users'),
            ('students', 'Students'),
            ('teachers', 'Teachers'),
            ('admins', 'Admins'),
        ),
        default='all'
    )
    is_active = models.BooleanField(default=True) # Admin can activate/deactivate

    def __str__(self):
        return self.title

    def is_visible_to(self, user):
        """Checks if the notification is visible to the given user based on their role."""
        if self.target_roles == 'all':
            return True
        elif self.target_roles == 'students' and user.is_student():
            return True
        elif self.target_roles == 'teachers' and user.is_teacher():
            return True
        elif self.target_roles == 'admins' and user.is_admin():
            return True
        return False
