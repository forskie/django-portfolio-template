from django.contrib import admin
from .models import Skill, Project, Experience, Profile, ContactLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role_title", "location")

    def has_add_permission(self, request):
        # Разрешаем создать запись только если её ещё нет — это singleton.
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "order")
    ordering = ("order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level")
    list_filter = ("category",)
    ordering = ("category", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "order")
    list_filter = ("status",)
    ordering = ("order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "place", "date_start", "date_end")
    ordering = ("-date_start",)