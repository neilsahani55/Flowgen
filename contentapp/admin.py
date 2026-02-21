from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_date', 'last_login_date', 'usage_count', 'subscription_type', 'company_name')
    list_filter = ('subscription_type', 'registration_date')
    search_fields = ('user__username', 'user__email', 'company_name', 'phone_number')
    readonly_fields = ('registration_date', 'last_login_date')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'registration_date', 'last_login_date')
        }),
        ('Profile Details', {
            'fields': ('usage_count', 'subscription_type', 'company_name', 'phone_number')
        }),
    )
    
    # This makes the admin load faster by preloading user data
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')