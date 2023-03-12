from rest_framework import serializers

from services.models import Subscriptions, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer() # вложенный сериалайзер
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')

    # дополнение сериализатора через MethodField. вычисления проводятся на питоне в таком случае
    price = serializers.SerializerMethodField()

    def get_price(self, instace):
        return (instace.service.full_price -
                instace.service.full_price * (instace.plan.discount_percent / 100))


    class Meta:
        model = Subscriptions
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
