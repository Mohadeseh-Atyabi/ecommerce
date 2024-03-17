from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.products.services import edit_order, delete_order, buy_product
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from ..models import Order


class OrderAPI(APIView):
    class OrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = '__all__'

    class InputBuySerializer(serializers.Serializer):
        quantity = serializers.IntegerField()

    @extend_schema(
        request=InputBuySerializer,
        responses=OrderSerializer,
    )
    def patch(self, req, pk):
        """
        Customer: Edit the quantity of an order.
        """
        input_serializer = self.InputBuySerializer(data=req.data)
        input_serializer.is_valid(raise_exception=True)
        order = edit_order(quantity=input_serializer.validated_data['quantity'], pk=pk)
        serializer = self.OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, req, pk):
        """
        Customer: Delete an order.
        """
        delete_order(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuyAPI(APIView):
    class OrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = '__all__'

    class EditOrderSerializer(serializers.Serializer):
        product_pk = serializers.IntegerField()
        quantity = serializers.IntegerField()

    @extend_schema(
        request=EditOrderSerializer,
        responses=OrderSerializer,
    )
    def post(self, req):
        """
        Customer: Add new order to his/her not paid payment.
        """
        input_serializer = self.EditOrderSerializer(data=req.data)
        input_serializer.is_valid(raise_exception=True)
        order = buy_product(quantity=input_serializer.validated_data['quantity'],
                            product_pk=input_serializer.validated_data['product_pk'], user=req.user)
        serializer = self.OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
