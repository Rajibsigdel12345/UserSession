from django.contrib import admin
from .models import User, AuthToken
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin panel
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    
    # Add filters based on these fields
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    
    # Add search functionality for these fields
    search_fields = ('username', 'email')
    
    # Organize fields into fieldsets for the detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name')
        }),
        ('Advanced Information', {
            'fields': ('username', 'email','is_active', 'is_staff', 'is_superuser','is_customer','is_seller','is_verified','provider')
        }),
    )

    # Make some fields read-only in the detail view
    readonly_fields = ('password',)

admin.site.register(User, UserAdmin)
admin.site.register(AuthToken)