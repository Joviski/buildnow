# coding=utf-8
"""Subscription App Models: Subscription Model."""
from collections import defaultdict
from datetime import timedelta, datetime
from decimal import Decimal
from locale import currency

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from . import SubscriptionPlan
from .subscription_plan import RecursionPlans, Currencies
from dateutil.relativedelta import relativedelta

class Subscription(models.Model):
    """Plans for subscription."""
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="subscriptions",
        related_query_name="subscription",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("User related to this subscription."),
    )
    plan = models.ForeignKey(
        "subscriptions.SubscriptionPlan",
        null=False,
        blank=False,
        related_name="subscriptions",
        related_query_name="subscription",
        on_delete=models.CASCADE,
        verbose_name=_("Plan"),
        help_text=_("Subscription Plan."),
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_("Active"),
        help_text=_("Determine the subscription status."),
    )
    iteration = models.IntegerField(
        default=1,
        verbose_name=_("Iteration")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Record Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Record Updated At")
    )

    class Meta:
        """Meta Class."""
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        unique_together = [
            ["user", "plan"]
        ]

    def __str__(self):
        """Override string method."""
        return f"{str(self.user)} - {str(self.plan)}"

    # def clean(self, ):
    #     """Override clean method."""
    #     super().clean()
    #     other_records = self.__class__.objects.filter(user=self.user, plan__service=self.plan.service, active=True)
    #     if self.pk:
    #         other_records = other_records.exclude(id=self.id)
    #     if other_records:
    #         raise ValidationError({'plan': f"This user is already subscribed to {str(self.plan.service)}."})

    def save(self, *args, **kwargs):
        """Override save method."""
        super().save(*args, **kwargs)

    @property
    def renewal_date(self):
        """Return the next renewal date."""
        if not self.pk:
            return None
        recursion_type = self.plan.recursion_type

        if recursion_type == RecursionPlans.MONTHLY:
            return self.created_at + relativedelta(months=self.iteration)
        elif recursion_type == RecursionPlans.ANNUALLY:
            return self.created_at + relativedelta(years=self.iteration)

    @property
    def remaining_days(self):
        """Return remaining days till next renewal."""
        if not self.renewal_date:
            return None
        delta = self.renewal_date.date() - timezone.now().date()
        return max(delta.days, 0)

    def switch_diff_month_to_annual(self, selected_currency=Currencies.SAR):
        """Calculate difference."""
        if self.plan.recursion_type != RecursionPlans.MONTHLY:
            return "0"
        annual_subscription_plan = SubscriptionPlan.objects.filter(
            service=self.plan.service,
            recursion_type=RecursionPlans.ANNUALLY,
            currency=selected_currency,
        ).last()
        if not annual_subscription_plan:
            return "-"

        monthly_plan = self.plan
        monthly_cost_per_year = monthly_plan.cost * 12

        return max(monthly_cost_per_year - annual_subscription_plan.cost, 0)

    @classmethod
    def get_last_6_months_subscription_spends(cls, user):
        """Get last 6 months spends."""
        today = datetime.now(timezone.utc)
        six_months_ago = today - timedelta(days=180)
        monthly_spend = defaultdict(Decimal)

        subscriptions = Subscription.objects.filter(user=user, plan__currency=Currencies.SAR)
        for subscription in subscriptions:
            iteration = subscription.iteration
            base_date = subscription.created_at

            for i in range(1, iteration + 1):
                if subscription.plan.recursion_type == RecursionPlans.MONTHLY:
                    renewal_date = base_date + relativedelta(months=i)
                elif subscription.plan.recursion_type == RecursionPlans.ANNUALLY:
                    renewal_date = base_date + relativedelta(years=i)
                else:
                    continue

                if six_months_ago <= renewal_date < today:
                    month_key = renewal_date.strftime("%Y-%m")
                    monthly_spend[month_key] += subscription.plan.cost

        return [{"month": month, "spend": spend, "currency": Currencies.SAR } for month, spend in sorted(monthly_spend.items())]
