# coding=utf-8
"""Subscription App Serializers: Subscription Plan Model Serializer."""

from rest_framework import serializers
from subscriptions.models import SubscriptionPlan

class SubscriptionPlanModelSerializer(serializers.ModelSerializer):
    """Subscription Plan Model Serializer."""
    recursion_type_display = serializers.SerializerMethodField()
    service = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        """Meta Class."""
        model = SubscriptionPlan
        fields = [
            'service',
            'recursion_type',
            'recursion_type_display',
            'cost',
            'currency',
        ]

    def get_recursion_type_display(self, obj):
        """Get recursion_type display."""
        return obj.get_recursion_type_display()

