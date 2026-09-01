from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, SystemSetting

def get_settings():
    setting, _ = SystemSetting.objects.get_or_create(id=1)
    return setting

# ------------------------------------------------------------------
# LOGIN & MANDATORY PASSWORD CHANGE
# ------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    system_setting = get_settings()

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            
            # Force first-login password change if default 123456 or flagged
            if profile.must_change_password or password == "123456":
                messages.warning(request, "First-time login detected. You must change your password to continue.")
                return redirect('force_change_password')

            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Full Name/Username or Password.")

    return render(request, 'portal/login.html', {'setting': system_setting})


@login_required
@require_http_methods(["GET", "POST"])
def force_change_password(request):
    """Forces user to change password from 123456 before accessing portal features"""
    if request.method == "POST":
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        if new_pass == "123456":
            messages.error(request, "Your new password cannot be the default password '123456'.")
        elif new_pass and new_pass == confirm_pass:
            request.user.set_password(new_pass)
            request.user.save()
            
            # Remove flag so user never has to change again unless requested
            profile = request.user.profile
            profile.must_change_password = False
            profile.save()

            update_session_auth_hash(request, request.user)
            messages.success(request, "Password updated successfully! Welcome to your portal.")
            return redirect('dashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'portal/change_password.html', {'setting': get_settings()})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been safely logged out.")
    return redirect('login')


# ------------------------------------------------------------------
# ISOLATED DASHBOARDS
# ------------------------------------------------------------------

@login_required
def dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    # Prevent bypassing password change screen
    if profile.must_change_password:
        return redirect('force_change_password')

    setting = get_settings()
    role = profile.role

    # ADMIN PORTAL (Full Control Over All Aspects)
    if role == 'ADMIN':
        all_users = UserProfile.objects.select_related('user').all()
        return render(request, 'portal/admin_dashboard.html', {
            'profile': profile,
            'setting': setting,
            'all_users': all_users,
        })

    # TEACHER PORTAL (Expanded Academic & Class Management Tools)
    elif role == 'TEACHER':
        return render(request, 'portal/teacher_dashboard.html', {
            'profile': profile,
            'setting': setting,
        })

    # STUDENT PORTAL (Isolated Personal Academic & Billing Portal)
    elif role == 'STUDENT':
        return render(request, 'portal/student_dashboard.html', {
            'profile': profile,
            'setting': setting,
        })

    return redirect('logout')


# ------------------------------------------------------------------
# ADMIN CONTROL ACTIONS
# ------------------------------------------------------------------

@login_required
@require_http_methods(["POST"])
def admin_update_theme(request):
    """Allows Admin to modify portal styling, colors, and announcements persistent across devices"""
    if request.user.profile.role != 'ADMIN':
        return redirect('dashboard')

    setting = get_settings()
    setting.school_name = request.POST.get('school_name', setting.school_name)
    setting.portal_accent_color = request.POST.get('portal_accent_color', setting.portal_accent_color)
    setting.secondary_color = request.POST.get('secondary_color', setting.secondary_color)
    setting.announcement_banner = request.POST.get('announcement_banner', setting.announcement_banner)
    setting.save()

    messages.success(request, "Portal appearance and global theme updated globally!")
    return redirect('dashboard')


@login_required
@require_http_methods(["POST"])
def admin_reset_user_password(request, user_id):
    """Admin feature to reset any user password back to 123456"""
    if request.user.profile.role != 'ADMIN':
        return redirect('dashboard')

    target_user = get_object_or_404(User, id=user_id)
    target_user.set_password("123456")
    target_user.save()

    profile = target_user.profile
    profile.must_change_password = True
    profile.save()

    messages.success(request, f"Password for {target_user.username} reset back to 123456.")
    return redirect('dashboard')