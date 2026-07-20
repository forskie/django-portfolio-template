from django.shortcuts import render
from .models import Skill, Project, Experience, Profile, ContactLink, Highlight, SiteSettings


def home(request):
    # Group skills by category, in the order defined by CATEGORY_CHOICES.
    # A group is only included once it has at least one row in the database.
    skill_groups = []
    for code, label in Skill.CATEGORY_CHOICES:
        skills = Skill.objects.filter(category=code)
        if skills.exists():
            skill_groups.append({"label": label, "skills": skills})

    context = {
        "profile": Profile.load(),
        "site_settings": SiteSettings.load(),
        "contact_links": ContactLink.objects.all(),
        "skill_groups": skill_groups,
        "projects": Project.objects.all(),
        "experiences": Experience.objects.all(),
        "highlights": Highlight.objects.all(),
    }
    return render(request, "main/home.html", context)