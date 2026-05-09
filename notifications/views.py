from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Notification
from .forms import NotificationForm
from accounts.views import is_admin # Import role test function

# --- Admin Views ---

@login_required
@user_passes_test(is_admin)
def create_notification(request):
    """
    Admin view to create a new notification or announcement.
    """
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.created_by = request.user
            notification.save()
            messages.success(request, 'Notification created successfully!')
            return redirect('notifications_list') # Redirect to list of notifications
    else:
        form = NotificationForm()
    return render(request, 'notifications/create_notification.html', {'form': form})

# --- Common Views (for all roles) ---

@login_required
def notifications_list(request):
    """
    View for all authenticated users to see notifications relevant to their role.
    """
    all_notifications = Notification.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter notifications based on the user's role
    user_notifications = [
        notification for notification in all_notifications
        if notification.is_visible_to(request.user)
    ]
    
    return render(request, 'notifications/notifications_list.html', {'notifications': user_notifications})
