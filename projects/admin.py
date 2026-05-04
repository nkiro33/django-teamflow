from django.contrib import admin

from .models import Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    autocomplete_fields = (
        "assigned_members",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "team",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "team",
        "start_date",
    )

    search_fields = (
        "name",
        "description",
        "team__name",
    )

    ordering = ("name",)

    autocomplete_fields = (
        "team",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = (
        TaskInline,
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "is_done",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_done",
        "project",
        "start_date",
        "end_date",
    )

    search_fields = (
        "title",
        "description",
        "project__name",
        "project__team__name",
    )

    ordering = (
        "is_done",
        "start_date",
        "title",
    )

    autocomplete_fields = (
        "project",
        "assigned_members",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )