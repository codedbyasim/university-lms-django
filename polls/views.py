from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q # Corrected import: import Q directly
from .models import Poll, Choice, Vote
from .forms import PollForm, ChoiceFormSet
from accounts.views import is_admin, is_student
from django.utils import timezone

# --- Admin Views ---

@login_required
@user_passes_test(is_admin)
def create_poll(request):
    """
    Admin view to create a new poll with choices.
    Uses a formset for choices.
    """
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST, instance=Poll()) # Instance is temporary for validation
        if poll_form.is_valid() and formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            formset.instance = poll # Associate choices with the newly created poll
            formset.save()
            messages.success(request, 'Poll created successfully!')
            return redirect('poll_list') # Redirect to general poll list for now
    else:
        poll_form = PollForm()
        formset = ChoiceFormSet(instance=Poll())
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form, 'formset': formset})

@login_required
@user_passes_test(is_admin)
def view_poll_results_admin(request):
    """
    Admin view to see results of all polls.
    """
    polls = Poll.objects.annotate(total_votes=Count('votes')).order_by('-created_at')
    return render(request, 'polls/poll_results_admin.html', {'polls': polls})

@login_required
@user_passes_test(is_admin)
def poll_detail_admin(request, pk):
    """
    Admin view for detailed poll results.
    """
    poll = get_object_or_404(Poll, pk=pk)
    choices = poll.choices.annotate(vote_count=Count('votes')).order_by('-vote_count')
    total_votes = sum(choice.vote_count for choice in choices)
    return render(request, 'polls/poll_detail_admin.html', {
        'poll': poll,
        'choices': choices,
        'total_votes': total_votes
    })

# --- Student Views ---

@login_required
@user_passes_test(is_student)
def poll_list(request):
    """
    Student view to list active polls they can vote in.
    """
    # Only show active polls that haven't ended and where the student hasn't voted yet
    active_polls = Poll.objects.filter(
        is_active=True,
        end_date__gte=timezone.now() # Polls that haven't ended yet
    ).exclude(
        votes__voter=request.user # Exclude polls where student has already voted
    ).order_by('-created_at')

    # Also show polls that have ended or where they have voted, to view results
    completed_or_voted_polls = Poll.objects.filter(
        Q(end_date__lt=timezone.now()) | Q(votes__voter=request.user) # Use Q directly
    ).distinct().order_by('-created_at')

    # Add a 'has_voted' attribute to each poll for easier template logic
    for poll in completed_or_voted_polls:
        poll.has_voted = Vote.objects.filter(poll=poll, voter=request.user).exists()


    return render(request, 'polls/poll_list.html', {
        'active_polls': active_polls,
        'completed_or_voted_polls': completed_or_voted_polls
    })


@login_required
@user_passes_test(is_student)
def vote_in_poll(request, pk):
    """
    Student view to cast a vote in a poll.
    """
    poll = get_object_or_404(Poll, pk=pk)

    # Check if poll is active and not ended
    if not poll.is_active or (poll.end_date and poll.end_date < timezone.now()):
        messages.error(request, "This poll is not active or has ended.")
        return redirect('poll_list')

    # Check if student has already voted
    if Vote.objects.filter(poll=poll, voter=request.user).exists():
        messages.warning(request, "You have already voted in this poll.")
        return redirect('poll_results', pk=pk) # Redirect to results if already voted

    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if not choice_id:
            messages.error(request, "Please select a choice.")
            return redirect('vote_in_poll', pk=pk)

        choice = get_object_or_404(Choice, pk=choice_id, poll=poll)
        Vote.objects.create(poll=poll, choice=choice, voter=request.user)
        messages.success(request, 'Your vote has been cast!')
        return redirect('poll_results', pk=pk) # Redirect to results after voting

    return render(request, 'polls/vote_in_poll.html', {'poll': poll})

@login_required
@user_passes_test(is_student)
def poll_results(request, pk):
    """
    Student view to see results of a specific poll.
    """
    poll = get_object_or_404(Poll, pk=pk)
    choices = poll.choices.annotate(vote_count=Count('votes')).order_by('-vote_count')
    total_votes = sum(choice.vote_count for choice in choices)

    # Check if student has voted in this poll
    has_voted = Vote.objects.filter(poll=poll, voter=request.user).exists()

    return render(request, 'polls/poll_results.html', {
        'poll': poll,
        'choices': choices,
        'total_votes': total_votes,
        'has_voted': has_voted
    })
