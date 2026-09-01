from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portal.views import home_portal, student_report_card

urlpatterns = [
    path('', home_portal, name='home_portal'),  # <--- Connects http://127.0.0.1:8000/
    path('admin/', admin.site.urls),
    path('report-card/<int:student_id>/', student_report_card, name='student_report_card'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)