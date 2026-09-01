from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.force_change_password, name='force_change_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/update-theme/', views.admin_update_theme, name='admin_update_theme'),
    path('admin/reset-password/<int:user_id>/', views.admin_reset_user_password, name='admin_reset_user_password'),
]