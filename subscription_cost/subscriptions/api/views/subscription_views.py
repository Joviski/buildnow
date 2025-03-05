# coding=utf-8
"""Subscription App Views: SubscriptionModelViewSet."""
from decimal import Decimal

from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from subscriptions.api.serializers import SubscriptionModelSerializer, CreateSubscriptionSerializer, SwitchSubscriptionPlanSerializer
from subscriptions.models import Subscription
from subscriptions.tasks import iterate_subscription

class SubscriptionModelViewSet(viewsets.ModelViewSet):
    """Subscription Model ViewSet."""
    authentication_classes = [BasicAuthentication]  # TODO: Replace with a more secure user based authentication. Ex. JWT
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionModelSerializer
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        """Override get_queryset method."""
        return Subscription.objects.filter(user=self.request.user)


    def create(self, request, *args, **kwargs):
        """Override create method."""
        serializer = CreateSubscriptionSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        subscription_obj = serializer.create(serializer.validated_data)

        if subscription_obj.active:
            iterate_subscription.s(subscription_obj.id).apply_async(eta=subscription_obj.renewal_date)

        return Response(data=self.serializer_class(subscription_obj).data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="switch_plans")
    def switch_plans(self, request):
        """Switch service plan."""
        serializer = SwitchSubscriptionPlanSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        subscription_obj = serializer.update(serializer.validated_data.get("subscription"), serializer.validated_data)


        return Response(data=self.serializer_class(subscription_obj).data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="monthly_expenses")
    def monthly_expenses(self, request):
        """Return monthly expenses aggregated."""
        total_subscription_costs = Subscription.objects.filter(active=True, user=request.user, plan__recursion_type= "MON", plan__currency="SAR").aggregate(Sum("plan__cost"))

        total_costs = Decimal(total_subscription_costs['plan__cost__sum'] or 0).quantize(Decimal("0.00"))
        return Response(data={"monthly_expenses": Subscription.get_last_6_months_subscription_spends(request.user)}, status=status.HTTP_200_OK)

