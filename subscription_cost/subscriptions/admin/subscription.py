# coding=utf-8
"""Subscription App Admin: Subscription Model Admin."""

from django.contrib import admin
from django.utils import formats
from subscriptions.models import Subscription

@admin.register(Subscription)
class SubscriptionModelAdmin(admin.ModelAdmin):
    """Subscription Model Admin."""
    list_display = [
        "user",
        "plan",
        "active",
        "renewal_date",
    ]
    readonly_fields = [
        "iteration",
        "created_at",
        "updated_at",
        "renewal_date",
    ]

    def renewal_date(self, obj):
        return formats.date_format(obj.renewal_date, "N j, Y, P")