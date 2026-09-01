from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_portal, name='home_portal'),
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('report-card/<int:student_id>/', views.student_report_card, name='student_report_card'),
]