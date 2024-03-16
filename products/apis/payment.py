from rest_framework.views import APIView
from products.serializers import PaymentSerializer
from products.services import get_payment, complete_payment
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


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
