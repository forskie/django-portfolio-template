from django.db import models


class Profile(models.Model):
    """
    Singleton: одна и только одна запись (pk всегда = 1).
    Хранит всё, что раньше было захардкожено в hero и в секции 'Currently'.
    Чтобы сделать такой же сайт под себя — просто меняешь эти поля в /admin/.
    """
    full_name = models.CharField(
        max_length=200, blank=True,
        help_text="Например: Safolov Biloliddin",
    )
    role_title = models.CharField(
        max_length=200, blank=True,
        help_text="Например: Backend Engineer",
    )
    location = models.CharField(
        max_length=200, blank=True,
        help_text="Например: Dushanbe, Tajikistan",
    )
    availability = models.CharField(
        max_length=200, blank=True,
        help_text="Например: Open to Remote (можно оставить пустым)",
    )
    thesis = models.TextField(
        blank=True,
        help_text="Короткий питч под именем в hero. "
                   "Можно оборачивать важные слова в <strong>...</strong> — они выделятся цветом.",
    )
    currently_text = models.TextField(
        blank=True,
        help_text="Текст секции 'Currently' внизу страницы. Можно использовать <strong>...</strong>.",
    )
    resume = models.FileField(
        upload_to="resume/", blank=True, null=True,
        help_text="Загрузи PDF — ссылка 'resume.pdf' в шапке будет вести на него",
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиль"

    def __str__(self):
        return self.full_name or "Профиль сайта"

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton — всегда одна запись
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # запрещаем удаление из кода (в админке тоже запрещено ниже)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactLink(models.Model):
    """
    Произвольные ссылки в шапке сайта: email, github, telegram, whatsapp,
    leetcode, телефон и т.д. Добавляются/убираются свободно из админки —
    сколько угодно штук, в любом порядке.
    """
    label = models.CharField(
        max_length=100,
        help_text="Текст ссылки, например: you@forskie.top или @Forck1e",
    )
    url = models.CharField(
        max_length=300,
        help_text=(
            "Полный адрес. Примеры: "
            "mailto:you@example.com · https://github.com/username · "
            "https://t.me/username · https://wa.me/992908204646 · "
            "tel:+992908204646 · https://leetcode.com/u/username"
        ),
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Контактная ссылка"
        verbose_name_plural = "Контактные ссылки"

    def __str__(self):
        return self.label


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("backend", "Backend"),
        ("tools", "Tools & DevOps"),
        ("soft", "Soft Skills"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.PositiveSmallIntegerField(help_text="1-5")

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("flagship", "Flagship"),
        ("in_progress", "In progress"),
        ("side", "Side project"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, help_text="Через запятую")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="side",
        help_text="Бейдж, который показывается на карточке проекта",
    )
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Experience(models.Model):
    place = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ["-date_start"]

    def __str__(self):
        return f"{self.role} @ {self.place}"