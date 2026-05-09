from django.db import models
from accounts.models import User

class Poll(models.Model):
    """
    Represents a poll created by an Admin.
    """
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) # Admins can activate/deactivate
    end_date = models.DateTimeField(null=True, blank=True) # Optional end date for polls

    def __str__(self):
        return self.question

class Choice(models.Model):
    """
    Represents a choice option within a poll.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.poll.question} - {self.choice_text}"

class Vote(models.Model):
    """
    Represents a student's vote for a poll choice.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'voter') # A student can vote only once per poll

    def __str__(self):
        return f"{self.voter.username} voted for '{self.choice.choice_text}' in '{self.poll.question}'"
