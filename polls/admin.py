from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    """Inline admin for Choices within a Poll."""
    model = Choice
    extra = 1 # Number of empty forms to display

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Admin interface for Poll model."""
    list_display = ('question', 'created_by', 'created_at', 'is_active', 'end_date')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question',)
    inlines = [ChoiceInline] # Allow adding choices directly when creating/editing a poll

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin interface for Vote model."""
    list_display = ('poll', 'choice', 'voter', 'voted_at')
    list_filter = ('poll', 'voter')
    search_fields = ('poll__question', 'voter__username')
    raw_id_fields = ('poll', 'choice', 'voter')
