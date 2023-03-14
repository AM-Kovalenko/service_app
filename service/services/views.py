from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscriptions
from services.serializers import SubscriptionSerializer


class SubscriptionsView(ReadOnlyModelViewSet):

    # queryset = Subscriptions.objects.all().prefetch_related('client').prefetch_related('client__user')

    # оптимизация квери запроса. убираем проблему n+1. bcgjkmpetv prefetch_related, чтоб не делать доп запросы
    # queryset = Subscriptions.objects.all().prefetch_related(
    #     'plan', 'service',
    #     Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
    #                                                                                  'user__email'))
    #
    # )

    queryset = Subscriptions.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email'))

    ).annotate(price=F('service__full_price') -
                     F('service__full_price') * F('plan__discount_percent') / 100.00)
    serializer_class = SubscriptionSerializer



    # переопределение метода list (в нем обрабатывается запрос и формируется ответ клиенту)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args,
                                **kwargs)  # обращение к базовому классу через super и возвращение(ничего не меняет)

        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data

        return response
