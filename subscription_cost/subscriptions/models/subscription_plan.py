# coding=utf-8
"""Subscription App Models: Subscription Plan Model."""

from django.db import models
from django.utils.translation import gettext_lazy as _

class RecursionPlans(models.TextChoices):
    """Recursion Plans."""
    MONTHLY = 'MON', 'Monthly'
    ANNUALLY = 'ANNU', 'Annually'

class Currencies(models.TextChoices):
    """Currency Choices."""
    SAR = 'SAR', 'SAR'

class SubscriptionPlan(models.Model):
    """Plans for subscription."""
    service = models.ForeignKey(
        "subscriptions.Service",
        null=False,
        blank=False,
        related_name="subscription_plans",
        related_query_name="subscription_plan",
        on_delete=models.CASCADE,
        verbose_name=_("Service"),
        help_text=_("Service related to this plan."),
    )
    recursion_type = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=RecursionPlans.choices,
        default=RecursionPlans.MONTHLY,
        verbose_name=_("Recursion Type"),
        help_text=_("Determine the type of this plan's recursion.")
    )
    currency = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=Currencies.choices,
        default=Currencies.SAR,
        verbose_name=_("Currency"),
        help_text=_("Determine the currency of this plan.")
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name=_("Cost"),
        help_text=_("How much this plan will cost.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("Record Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_("Record Updated At")
    )

    class Meta:
        """Meta Class."""
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")
        unique_together = [
            ["service", "recursion_type", "currency"]
        ]

    def __str__(self):
        """Override string method."""
        return f"{str(self.service)} - {str(self.get_recursion_type_display())} - Cost: {self.cost} {self.currency}"
