from django.db import models


class Profile(models.Model):
    """
    Singleton: exactly one row (pk is always 1).
    Everything shown in the hero and the 'Currently' section lives here.
    To reuse this template for yourself, just edit these fields in /admin/.
    """
    full_name = models.CharField(
        max_length=200, blank=True,
        help_text="E.g. Jane Doe",
    )
    role_title = models.CharField(
        max_length=200, blank=True,
        help_text="E.g. Backend Engineer",
    )
    location = models.CharField(
        max_length=200, blank=True,
        help_text="E.g. Dushanbe, Tajikistan (leave blank to hide)",
    )
    availability = models.CharField(
        max_length=200, blank=True,
        help_text="E.g. Open to remote work (leave blank to hide)",
    )
    thesis = models.TextField(
        blank=True,
        help_text="Short pitch under the name in the hero. "
                   "Wrap key words in <strong>...</strong> to highlight them in accent color.",
    )
    currently_text = models.TextField(
        blank=True,
        help_text="Text for the 'Currently' section. <strong>...</strong> is supported.",
    )
    photo = models.ImageField(
        upload_to="profile/", blank=True, null=True,
        help_text="Optional headshot for the hero. Square images (min 480x480) work best.",
    )
    resume = models.FileField(
        upload_to="resume/", blank=True, null=True,
        help_text="Upload a PDF — the 'Resume' button in the hero will link to it.",
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name or "Site profile"

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton — always one row
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # deletion disabled in code (and in the admin below)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactLink(models.Model):
    """
    Links rendered as buttons in the hero: email, GitHub, LinkedIn, Telegram,
    a phone number, etc. Add or remove as many as you like, in any order.
    """
    ICON_CHOICES = [
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("telegram", "Telegram"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("whatsapp", "WhatsApp"),
        ("website", "Website"),
        ("link", "Generic link"),
    ]
    label = models.CharField(
        max_length=100,
        help_text="Button text, e.g. you@example.com or @username",
    )
    url = models.CharField(
        max_length=300,
        help_text=(
            "Full address. Examples: mailto:you@example.com · "
            "https://github.com/username · https://t.me/username · "
            "https://wa.me/15551234567 · tel:+15551234567"
        ),
    )
    icon = models.CharField(
        max_length=20, choices=ICON_CHOICES, default="link",
        help_text="Which icon to show next to the label.",
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Primary buttons are styled as solid/filled (use for one main CTA, e.g. Email).",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Contact link"
        verbose_name_plural = "Contact links"

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
    level = models.PositiveSmallIntegerField(
        blank=True, null=True,
        help_text="Optional, 1-5. Leave blank to hide the level indicator for this skill.",
    )

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

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
    tech_stack = models.CharField(max_length=300, help_text="Comma-separated, e.g. Django, PostgreSQL, Redis")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="side",
        help_text="Badge shown on the project card.",
    )
    thumbnail = models.ImageField(
        upload_to="projects/", blank=True, null=True,
        help_text="Optional cover image, shown at the top of the card (recommended 16:9).",
    )
    logo = models.ImageField(
        upload_to="projects/logos/", blank=True, null=True,
        help_text="Optional small square logo, shown next to the title instead of a thumbnail.",
    )
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class Experience(models.Model):
    place = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True, help_text="Leave blank for 'Present'.")
    description = models.TextField()

    class Meta:
        ordering = ["-date_start"]
        verbose_name = "Experience"
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.role} @ {self.place}"


class Highlight(models.Model):
    """
    Flexible entries for education, certifications, or achievements.
    Replaces the old hardcoded 'deployment' block. Fully optional — the
    section is hidden entirely if no highlights are added.
    """
    TYPE_CHOICES = [
        ("education", "Education"),
        ("certification", "Certification"),
        ("achievement", "Achievement"),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200, help_text="E.g. B.Sc. Computer Science, or AWS Certified Developer")
    subtitle = models.CharField(max_length=200, blank=True, help_text="E.g. institution or issuing organization")
    description = models.TextField(blank=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True, help_text="Leave blank for ongoing / no end date.")
    url = models.URLField(blank=True, help_text="Optional link, e.g. to a credential or certificate.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date_start"]
        verbose_name = "Highlight"
        verbose_name_plural = "Highlights"

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """
    Singleton: site-wide SEO metadata, footer text, and the optional
    deployment status panel. Edit in /admin/.
    """
    meta_description = models.TextField(
        blank=True,
        help_text="Used for the meta description and social previews. "
                   "If left blank, profile.thesis is used instead.",
    )
    meta_keywords = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(
        upload_to="seo/", blank=True, null=True,
        help_text="Image shown when the site is shared on social media (recommended 1200x630).",
    )
    favicon = models.ImageField(upload_to="seo/", blank=True, null=True)
    twitter_handle = models.CharField(max_length=100, blank=True, help_text="E.g. @username (leave blank to omit)")
    canonical_url = models.URLField(
        blank=True,
        help_text="Full site URL, e.g. https://example.com. If blank, the current request URL is used.",
    )
    footer_text = models.CharField(
        max_length=300, blank=True,
        help_text="Overrides the default footer text. If blank, shows '© {year} {full name}'.",
    )

    show_deployment_panel = models.BooleanField(
        default=False,
        help_text="Show an optional 'deployment status' panel in the footer.",
    )
    deployment_host = models.CharField(max_length=100, blank=True)
    deployment_server = models.CharField(max_length=100, blank=True)
    deployment_runtime = models.CharField(max_length=100, blank=True)
    deployment_database = models.CharField(max_length=100, blank=True)
    deployment_proxy = models.CharField(max_length=100, blank=True)
    deployment_shipped_via = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def deployment_fields(self):
        """List of (label, value) pairs for populated deployment fields only."""
        pairs = [
            ("Host", self.deployment_host),
            ("Server", self.deployment_server),
            ("Runtime", self.deployment_runtime),
            ("Database", self.deployment_database),
            ("Proxy", self.deployment_proxy),
            ("Shipped via", self.deployment_shipped_via),
        ]
        return [(label, value) for label, value in pairs if value]