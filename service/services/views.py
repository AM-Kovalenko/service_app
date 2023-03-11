from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscriptions
from services.serializers import SubscriptionSerializer


class SubscriptionsView(ReadOnlyModelViewSet):
    # оптимизация квери запроса. убираем проблему n+1. bcgjkmpetv prefetch_related, чтоб не делать доп запросы
    # queryset = Subscriptions.objects.all().prefetch_related('client').prefetch_related('client__user')

    queryset = Subscriptions.objects.all().prefetch_related(
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email'))

    )
    serializer_class = SubscriptionSerializer
