"""
Models for the Portfolio application.
Defines Project and ContactMessage data structures.
"""
from django.db import models
from django.utils import timezone


class Project(models.Model):
    """
    Represents a portfolio project displayed on the Projects page.
    Manageable via Django admin panel.
    """
    title = models.CharField(max_length=200, help_text="Project title")
    description = models.TextField(help_text="Detailed project description")
    short_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Short summary shown on project cards"
    )
    tech_stack = models.CharField(
        max_length=500,
        help_text="Comma-separated tech stack (e.g. 'Python, Django, PostgreSQL')"
    )
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Project screenshot or thumbnail"
    )
    github_url = models.URLField(blank=True, null=True, help_text="GitHub repository link")
    live_url = models.URLField(blank=True, null=True, help_text="Live demo / deployed URL")
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured projects appear on the Home page"
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def get_tech_list(self):
        """Returns tech_stack as a Python list for template iteration."""
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]


class ContactMessage(models.Model):
    """
    Stores contact form submissions from website visitors.
    """
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=300, blank=True, default="Portfolio Contact")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, help_text="Mark as read in admin")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} ({self.email}) — {self.created_at.strftime('%d %b %Y')}"
