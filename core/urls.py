from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Direct main domain (/) straight to the Portal Login
    path('', lambda request: redirect('login'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
]