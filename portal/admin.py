from django.contrib import admin
from django.utils.html import format_html
from .models import SchoolBranding, TeacherProfile, ClassSection, Student, SubjectResult

class SubjectResultInline(admin.TabularInline):
    model = SubjectResult
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'first_name', 'last_name', 'class_section', 'view_report_card')
    inlines = [SubjectResultInline]

    def view_report_card(self, obj):
        if obj.id:
            return format_html('<a class="button" href="/report-card/{}/" target="_blank" style="background:#007bff; color:white; padding:3px 8px; border-radius:3px; text-decoration:none;">📄 View Report Card</a>', obj.id)
        return ""
    
    view_report_card.short_description = "Report Card"

admin.site.register(SchoolBranding)
admin.site.register(TeacherProfile)
admin.site.register(ClassSection)
admin.site.register(SubjectResult)