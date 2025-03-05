# coding=utf-8
"""Subscription App Admin: Subscription Plan Model Admin."""

from django.contrib import admin
from subscriptions.models import SubscriptionPlan

@admin.register(SubscriptionPlan)
class SubscriptionPlanModelAdmin(admin.ModelAdmin):
    """SubscriptionPlan Model Admin."""
    list_display = [
        "service",
        "recursion_type",
        "cost",
        "currency",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]