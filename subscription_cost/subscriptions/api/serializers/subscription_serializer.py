# coding=utf-8
"""Subscription App Serializers: Subscription Model Serializer."""

from rest_framework import serializers
from subscriptions.models import Subscription, Service, SubscriptionPlan
from subscriptions.models.subscription_plan import RecursionPlans
from .plan_serializer import SubscriptionPlanModelSerializer

class CreateSubscriptionSerializer(serializers.Serializer):
    """Create Subscription Serializer."""
    service = serializers.CharField(required=True)
    recursion_type = serializers.ChoiceField(required=True, choices=[choice[0] for choice in RecursionPlans.choices])

    def validate(self, attrs):
        """Override validate method."""
        service_name = attrs.get("service")
        recursion_type = attrs.get("recursion_type")
        choices = list(Service.objects.values_list("name", flat=True))
        if service_name not in choices:
            raise serializers.ValidationError({"errors": "Invalid choice."})
        user = self.context.get("user")
        service = Service.objects.get(name=service_name)
        subscription_plan = SubscriptionPlan.objects.filter(service=service, recursion_type=recursion_type).last()
        if not subscription_plan:
            raise serializers.ValidationError({"errors": "This service doesn't offer this plan."})
        if Subscription.objects.filter(user=user, plan__service=service, active=True).exists():
            raise serializers.ValidationError({"errors": f"This user is already subscribed to {str(service)}."})

        validated_data = {
            "user": user,
            "plan": subscription_plan,
            "active": True,
        }
        return validated_data

    def create(self, validated_data):
        """Override create."""
        return Subscription.objects.create(
            **validated_data
        )


class SwitchSubscriptionPlanSerializer(serializers.Serializer):
    """Create Subscription Serializer."""
    service = serializers.CharField(required=True)
    recursion_type = serializers.ChoiceField(required=True, choices=[choice[0] for choice in RecursionPlans.choices])

    def validate(self, attrs):
        """Override validate method."""
        service_name = attrs.get("service")
        recursion_type = attrs.get("recursion_type")
        choices = list(Service.objects.values_list("name", flat=True))
        if service_name not in choices:
            raise serializers.ValidationError({"errors": "Invalid choice."})
        user = self.context.get("user")
        service = Service.objects.get(name=service_name)
        subscription_plan = SubscriptionPlan.objects.filter(service=service, recursion_type=recursion_type, currency="SAR").last()
        if not subscription_plan:
            raise serializers.ValidationError({"errors": "This service doesn't offer this plan."})
        subscription = Subscription.objects.filter(user=user, plan__service=service, active=True).last()
        if not subscription:
            raise serializers.ValidationError({"errors": "This user is not subscribed to this service."})
        if subscription and subscription.plan.recursion_type == recursion_type:
            raise serializers.ValidationError({"errors": "This user is already subscribed to this plan."})

        validated_data = {
            "plan": subscription_plan,
            "subscription": subscription,
        }
        return validated_data

    def update(self, instance, validated_data):
        """Override create."""

        subscription_plan = validated_data.get("plan")

        instance.plan = subscription_plan
        instance.save(update_fields=["plan"])

        return instance




class SubscriptionModelSerializer(serializers.ModelSerializer):
    """Subscription Model Serializer."""
    plan = SubscriptionPlanModelSerializer()
    class Meta:
        """Meta Class"""
        model = Subscription
        fields = [
            "id",
            "user",
            "plan",
            "iteration",
            "renewal_date",
            "remaining_days",
            "switch_diff_month_to_annual",
        ]

