from django.db import models
from django.contrib.auth.models import User

# 1. School Branding (Logos & Motto)
class SchoolBranding(models.Model):
    school_name = models.CharField(max_length=150, default="Al-Wasilah School")
    school_motto = models.CharField(max_length=150, default="Knowledge for Service")
    logo_header = models.ImageField(upload_to='branding/', blank=True, null=True)
    logo_print = models.ImageField(upload_to='branding/', blank=True, null=True)

    def __str__(self):
        return self.school_name

# 2. Teacher Profile
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    signature_image = models.ImageField(upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return self.full_name

# 3. Class Section
class ClassSection(models.Model):
    class_name = models.CharField(max_length=50) # e.g., "Basic 8A"
    academic_year = models.CharField(max_length=10) # e.g., "2025/2026"
    class_teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.class_name} ({self.academic_year})"

# 4. Student Profile
class Student(models.Model):
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"

# 5. Subject & Student Grade Entry
class SubjectResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject_name = models.CharField(max_length=100)
    ca_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    @property
    def total_score(self):
        return self.ca_score + self.exam_score

    @property
    def grade(self):
        total = self.total_score
        if total >= 75:
            return 'A1'
        elif total >= 70:
            return 'B2'
        elif total >= 65:
            return 'B3'
        elif total >= 60:
            return 'C4'
        elif total >= 55:
            return 'C5'
        elif total >= 50:
            return 'C6'
        elif total >= 45:
            return 'D7'
        elif total >= 40:
            return 'E8'
        else:
            return 'F9'

    def __str__(self):
        return f"{self.student.first_name} - {self.subject_name}: {self.total_score}"