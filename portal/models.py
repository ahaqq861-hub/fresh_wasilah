from django.db import models
from django.contrib.auth.models import User

# Role choices
ROLE_CHOICES = (
    ('ADMIN', 'Administrator'),
    ('TEACHER', 'Teacher'),
    ('STUDENT', 'Student'),
)

class SystemSetting(models.Model):
    """Stores global portal branding and appearance controlled by Admin"""
    school_name = models.CharField(default="UDS Fresh Wasilah Campus Portal", max_length=200)
    portal_accent_color = models.CharField(default="#006633", max_length=20) # UDS Green
    secondary_color = models.CharField(default="#ffcc00", max_length=20)     # UDS Gold/Yellow
    announcement_banner = models.TextField(blank=True, default="Welcome to Fresh Wasilah Portal. Please complete registration.")
    login_subtext = models.CharField(default="University for Development Studies - Student & Staff Authentication", max_length=255)

    def __str__(self):
        return "Portal Customization & System Settings"

class UserProfile(models.Model):
    """Extended user attributes including first-time password reset flag"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    must_change_password = models.BooleanField(default=True)  # Forces change from 123456
    id_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    department_or_class = models.CharField(max_length=100, blank=True, default="Banking and Finance")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"