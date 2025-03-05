# coding=utf-8
"""Subscription App Models: Services Model."""

from django.db import models
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    """Services available for subscription."""
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("Service Name"),
        help_text=_("The name/title of the service.")
    )
    description = models.TextField(
        null=False,
        blank=True,
        verbose_name=_("Service Description"),
        help_text=_("More info about this service.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("Record Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_("Record Updated At")
    )

    class Meta:
        """Meta Class."""
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        """Override string method."""
        return self.name
