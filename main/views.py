from django.shortcuts import render
from .models import Skill, Project, Experience, Profile, ContactLink


def home(request):
    # Группируем навыки по категориям в порядке, заданном в CATEGORY_CHOICES.
    # Группа не выводится, если в ней ещё нет ни одной записи в БД.
    skill_groups = []
    for code, label in Skill.CATEGORY_CHOICES:
        skills = Skill.objects.filter(category=code)
        if skills.exists():
            skill_groups.append({"label": label, "skills": skills})

    context = {
        "profile": Profile.load(),
        "contact_links": ContactLink.objects.all(),
        "skill_groups": skill_groups,
        "projects": Project.objects.all(),
        "experiences": Experience.objects.all(),
    }
    return render(request, "main/home.html", context)

