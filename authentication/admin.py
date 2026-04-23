from django.contrib import admin
from .models import LoginAttempt, UserProfile


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
	list_display = ('username', 'ip_address', 'failed_attempts', 'locked_until', 'last_attempt_at')
	search_fields = ('username', 'ip_address')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'role', 'phone_number', 'created_at')
	list_filter = ('role',)
	search_fields = ('user__username',)
