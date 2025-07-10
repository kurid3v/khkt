from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),  # ✅ Phải có tên 'home'
    path('problems/', include('problems.urls')),
    path('submissions/', include('submissions.urls')),
    path('users/', include('users.urls')),
    path('submissions/', include('submissions.urls')),
    path('exams/', include('exams.urls')),
]
