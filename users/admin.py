from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    # Forms para adicionar e alterar instâncias do modelo CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Campos que aparecem no admin
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password")}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('slug', 'photo', 'created', 'updated', 'user')
    list_filter = ('photo', 'slug', 'created', 'updated', 'user')

admin.site.register(CustomUser, CustomUserAdmin)
