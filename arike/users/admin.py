from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from arike.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("full_name", "phone","role", "gender","district")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_verified",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role','password1', 'password2'),
        }),
    )
    list_filter = ('role','is_staff', 'is_superuser', 'is_active', 'groups')
    list_display = ["email", "full_name","role", "is_superuser"]
    search_fields = ["full_name"]