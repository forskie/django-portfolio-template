from django.contrib import admin
from .models import (
    Skill, Project, Experience, Profile, ContactLink, Highlight, SiteSettings,
)


class SingletonAdmin(admin.ModelAdmin):
    """Shared behavior for Profile and SiteSettings: exactly one row, never deletable."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Profile)
class ProfileAdmin(SingletonAdmin):
    list_display = ("full_name", "role_title", "location")


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ("__str__", "show_deployment_panel")
    fieldsets = (
        ("SEO", {
            "fields": ("meta_description", "meta_keywords", "og_image", "favicon",
                       "twitter_handle", "canonical_url"),
        }),
        ("Footer", {
            "fields": ("footer_text",),
        }),
        ("Deployment panel (optional)", {
            "fields": ("show_deployment_panel", "deployment_host", "deployment_server",
                       "deployment_runtime", "deployment_database", "deployment_proxy",
                       "deployment_shipped_via"),
        }),
    )


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "icon", "is_primary", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level")
    list_filter = ("category",)
    ordering = ("category", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "order")
    list_editable = ("order",)
    list_filter = ("status",)
    ordering = ("order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "place", "date_start", "date_end")
    ordering = ("-date_start",)


@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "subtitle", "date_start", "date_end", "order")
    list_editable = ("order",)
    list_filter = ("type",)
    ordering = ("order", "-date_start")