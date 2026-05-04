from django.contrib import admin

from .models import Team, TeamMembership


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
    autocomplete_fields = ("user",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = ("name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = (
        TeamMembershipInline,
    )


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "user",
        "role",
        "created_at",
    )

    list_filter = (
        "role",
        "team",
    )

    search_fields = (
        "team__name",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    autocomplete_fields = (
        "team",
        "user",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )