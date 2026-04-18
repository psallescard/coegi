from django.contrib import admin

from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_pinned", "created_at")
    list_filter = ("is_pinned", "owner")
    search_fields = ("name", "owner__username")
    ordering = ("-is_pinned", "-created_at")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "user", "status", "position", "last_status_change")
    list_filter = ("status", "project", "user")
    search_fields = ("name", "note", "user__username")
    ordering = ("status", "position", "-last_status_change")
    readonly_fields = ("created_at", "updated_at", "last_status_change")
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("user", "project", "name", "note"),
            },
        ),
        (
            "Flow & Status",
            {
                "fields": ("status", "position", "last_status_change"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
