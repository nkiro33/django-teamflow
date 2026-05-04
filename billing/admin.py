from django.contrib import admin

from .models import SubscriptionPlan, TeamSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "billing_interval",
        "max_projects",
        "max_team_members",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "billing_interval",
        "is_active",
    ]
    search_fields = [
        "name",
        "description",
    ]
    ordering = ["price"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]


@admin.register(TeamSubscription)
class TeamSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "team",
        "plan",
        "status",
        "starts_at",
        "ends_at",
        "created_at",
    ]
    list_filter = [
        "status",
        "plan",
    ]
    search_fields = [
        "team__name",
        "plan__name",
    ]
    autocomplete_fields = [
        "team",
        "plan",
    ]
    ordering = ["-created_at"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]