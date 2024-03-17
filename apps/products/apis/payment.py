from rest_framework.views import APIView
from apps.products.services import get_payment, complete_payment
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from ..models import Order, Payment


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(source='order_set', many=True, read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    class Meta:
        model = Payment
        fields = ['id', 'status', 'total_price', 'customer', 'orders']

    def get_total_price(self, obj):
        total_price = 0
        for order in obj.order_set.all():
            total_price += order.calculate_price()
        return total_price


class PaymentAPI(APIView):
    @extend_schema(
        responses=PaymentSerializer,
    )
    def get(self, req):
        """
        Customer: View list of customer's payments.
        """
        payments = get_payment(data={'user': req.user})
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PayPaymentAPI(APIView):
    @extend_schema(
        responses=PaymentSerializer,
    )
    def get(self, req):
        """
        Customer: View customer's not paid payment.
        """
        payment = get_payment(data={'customer': req.user, 'status': False})
        serializer = PaymentSerializer(instance=payment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompletePaymentAPI(APIView):
    @extend_schema(
        responses=PaymentSerializer,
    )
    def get(self, req):
        """
        Customer: Pay a payment to complete it.
        """
        payment = complete_payment(user=req.user)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
