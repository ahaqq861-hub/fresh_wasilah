from django.shortcuts import render, get_object_or_404
from .models import Student, SchoolBranding

def home_portal(request):
    students = Student.objects.all()
    # Fetch the branding details using the correct model name
    branding = SchoolBranding.objects.first()
    
    return render(request, 'portal/home.html', {
        'students': students,
        'branding': branding
    })

def student_report_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    branding = SchoolBranding.objects.first()
    
    return render(request, 'portal/report_card.html', {
        'student': student,
        'branding': branding
    })