# coding=utf-8
"""Subscription App Admin: Services Model Admin."""

from django.contrib import admin
from subscriptions.models import Service

@admin.register(Service)
class ServiceModelAdmin(admin.ModelAdmin):
    """Service Model Admin."""
    readonly_fields = [
        "created_at",
        "updated_at",
    ]