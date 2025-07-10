from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_teacher', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Loại tài khoản', {'fields': ('is_teacher',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
