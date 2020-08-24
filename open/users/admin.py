from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from open.core.betterself.utilities.demo_user_factory_fixtures import (
    create_demo_fixtures_for_user,
)
from open.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


admin.site.site_header = "Open Control Panel"


def create_demo_fixtures(modeladmin, request, queryset):
    for instance in queryset:
        create_demo_fixtures_for_user(instance)


create_demo_fixtures.short_description = "Create Demo Fixtures"


class TokenInline(admin.TabularInline):
    model = Token


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = [
        "username",
        "email",
        "signed_up_from",
        "created",
        "modified",
    ]
    search_fields = ["name", "email"]
    inlines = [TokenInline]
    actions = [create_demo_fixtures]
    ordering = ["-id"]
