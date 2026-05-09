import base64
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.base import ContentFile
from django.conf import settings # Import settings to access MEDIA_ROOT
from django.http import JsonResponse # Import JsonResponse
from .forms import AdminUserCreationForm, LoginForm, UserProfileForm
from .models import User
from departments.models import Department, Program # Import Department and Program

# Test functions for user_passes_test decorator
def is_admin(user):
    """Checks if the user is an Admin."""
    return user.is_authenticated and user.is_admin()

def is_teacher(user):
    """Checks if the user is a Teacher."""
    return user.is_authenticated and user.is_teacher()

def is_student(user):
    """Checks if the user is a Student."""
    return user.is_authenticated and user.is_student()

def is_department_manager(user):
    """Checks if the user is a Department Manager."""
    return user.is_authenticated and user.is_department_manager()

def login_view(request):
    """
    Handles user login.
    Redirects to the appropriate dashboard based on user role upon successful login.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard_view(request):
    """
    Redirects authenticated users to their respective dashboards based on their role.
    """
    if request.user.is_admin():
        return redirect('admin_dashboard')
    elif request.user.is_department_manager(): # New role check
        return redirect('department_manager_dashboard')
    elif request.user.is_teacher():
        return redirect('teacher_dashboard')
    elif request.user.is_student():
        return redirect('student_dashboard')
    return redirect('login') # Fallback in case of unhandled role

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Admin dashboard view. Accessible only by Admin users.
    """
    return render(request, 'accounts/admin_dashboard.html')

@login_required
@user_passes_test(is_department_manager) # Accessible only by Department Managers
def department_manager_dashboard(request):
    """
    Department Manager dashboard view.
    """
    return render(request, 'accounts/department_manager_dashboard.html')


@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    """
    Teacher dashboard view. Accessible only by Teacher users.
    """
    return render(request, 'accounts/teacher_dashboard.html')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    """
    Student dashboard view. Accessible only by Student users.
    """
    return render(request, 'accounts/student_dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_create_user(request):
    """
    Admin view to create new user accounts (Admin, Teacher, or Student).
    """
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User '{user.username}' with role '{user.get_role_display()}' created successfully!")
            return redirect('admin_create_user') # Redirect back to admin dashboard, or to a user list if you create one
        else:
            messages.error(request, "Error creating user. Please check the form.")
    else:
        form = AdminUserCreationForm()
    
    context = {
        'form': form,
        # departments and programs are now handled by form/AJAX, no need to pass all here
    }
    return render(request, 'accounts/admin_create_user.html', context)

@login_required
def profile_view(request):
    """
    View for users to see and edit their profile details, including profile image.
    Handles cropped image data from Cropper.js.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        
        # Handle cropped image data if present
        cropped_image_data = request.POST.get('cropped_image_data')
        if cropped_image_data:
            format, imgstr = cropped_image_data.split(';base64,') # e.g., data:image/jpeg,base64,ABC...
            ext = format.split('/')[-1] # e.g., jpeg
            
            # Generate a unique filename
            import uuid
            file_name = f"{request.user.username}_{uuid.uuid4()}.{ext}"
            
            # Decode base64 string and create ContentFile
            data = ContentFile(base64.b64decode(imgstr), name=file_name)
            
            # Assign the new file to the profile_image field
            # If an old image exists, it will be replaced by Django's FileField logic
            request.user.profile_image.save(file_name, data, save=False)
            
        if form.is_valid():
            form.save() # Save the form data, including the profile_image if it was set above
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile. Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def change_password_view(request):
    """
    View for users to change their password.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Updates the user's session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile') # Redirect to profile after password change
        else:
            messages.error(request, 'Please correct the error below. Your password was not changed.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
@user_passes_test(is_admin) # Only admins should access this
def get_programs_by_department(request):
    """
    AJAX view to return programs belonging to a selected department.
    """
    department_id = request.GET.get('department_id')
    programs = []
    if department_id:
        programs_qs = Program.objects.filter(department_id=department_id).order_by('name')
        for program in programs_qs:
            programs.append({'id': program.id, 'name': program.name})
    return JsonResponse({'programs': programs})
