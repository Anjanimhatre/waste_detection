from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'city', 'is_staff', 'is_active')
    list_filter = ('role', 'city', 'is_staff', 'is_active')  # Filter users by city
    search_fields = ('username', 'email', 'city')
    ordering = ('city', 'username')  # Order by city first, then username

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'city', 'role'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'location', 'uploaded_at', 'cleaned_by')
    list_filter = ('city', 'uploaded_at')  # Filter images by city
    search_fields = ('user__username', 'city', 'location')

    def get_queryset(self, request):
        """Show only images uploaded in the city manager's city"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Show all images for superuser
        elif request.user.role == "city_manager":
            return qs.filter(city=request.user.city)  # Show only images from the city manager's city
        return qs.none()  # Other users can't see images

admin.site.register(UploadedImage, UploadedImageAdmin)