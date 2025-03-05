"""Paymob Onboarding: URLs."""

from rest_framework.routers import SimpleRouter
from subscriptions.api.views.subscription_views import SubscriptionModelViewSet

subscription_router = SimpleRouter(trailing_slash=True)

subscription_router.register(
    "",
    SubscriptionModelViewSet,
    basename="subscriptions",
)
urlpatterns = []  # type: ignore
