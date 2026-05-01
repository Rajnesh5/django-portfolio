"""
Admin configuration for Portfolio models.
Provides a rich admin interface for managing Projects and Contact Messages.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ContactMessage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'tech_stack_preview', 'is_featured', 'order', 'created_at', 'view_links']
    list_filter = ['is_featured', 'created_at']
    list_editable = ['is_featured', 'order']
    search_fields = ['title', 'description', 'tech_stack']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'short_description', 'image')
        }),
        ('Technical Details', {
            'fields': ('tech_stack',)
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order', 'created_at')
        }),
    )

    def tech_stack_preview(self, obj):
        """Show first 50 chars of tech stack."""
        return obj.tech_stack[:60] + '...' if len(obj.tech_stack) > 60 else obj.tech_stack
    tech_stack_preview.short_description = 'Tech Stack'

    def view_links(self, obj):
        """Clickable links to GitHub and live demo."""
        links = []
        if obj.github_url:
            links.append(f'<a href="{obj.github_url}" target="_blank">GitHub</a>')
        if obj.live_url:
            links.append(f'<a href="{obj.live_url}" target="_blank">Live</a>')
        return format_html(' | '.join(links)) if links else '—'
    view_links.short_description = 'Links'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        """Prevent manually adding messages from admin."""
        return False


# Customize admin site branding
admin.site.site_header = "Rajnesh Kr. Ranjan — Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Admin Panel"
