from django.contrib import admin

from users.models import CustomUser

from users.forms import CustomUserCreationForm, CustomUserChangeForm



class CustomUserAdmin(admin.ModelAdmin):
    model=CustomUser
    form=CustomUserCreationForm
    add_form=CustomUserChangeForm

    list_display = ["email", "username", "is_staff", "is_superuser"]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    ordering = ["email"]
    search_fields = ["email", "username"]
    fieldsets = [
        (None, {"fields": ["email", "username", "password"]}),
        ("permisos", {"fields": ["is_staff", "is_superuser", "is_active", "groups", "user_permissions"]}),
        ("fechas", {"fields": ["last_login", "date_joined"]}),
    ]


admin.site.register(CustomUser, CustomUserAdmin)
