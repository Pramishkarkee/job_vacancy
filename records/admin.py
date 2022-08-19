from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from django.forms.widgets import CheckboxSelectMultiple

from records.models import User, Applicant, Provider


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    personal_info = (
        "Personal Information",
        {
            "fields": (
                "first_name",
                "middle_name",
                "last_name",
                "contact_number",
                "profile_photo",
                "is_registered",
                "profile_type",
            )
        },
    )

    fieldsets = (
        ("Login Information", {"fields": ("username", "email", "password")}),
        personal_info,
    )

    add_fieldsets = (
        (
            "Login Information",
            {"fields": ("username", "email", "password1", "password2")},
        ),
        personal_info,
    )


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Personal Information", {"fields": ("id", "gender", "date_of_birth")}),
        ("Address Information", {"fields": ("temporary_address", "permanent_address")}),
        (
            "Professional Information",
            {
                "fields": (
                    "qualification",
                    "skills",
                    "experience",
                    "cv",
                    "supporting_document",
                    "profile_links",
                    "employment_status",
                    "interested_categories",
                ),
            },
        ),
    )

    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
