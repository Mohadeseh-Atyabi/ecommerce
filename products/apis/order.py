from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from products.serializers import OrderSerializer, InputBuySerializer, EditOrderSerializer
from products.services import edit_order, delete_order, buy_product
from drf_spectacular.utils import extend_schema


class OrderAPI(APIView):
    @extend_schema(
        request=InputBuySerializer,
        responses=OrderSerializer,
    )
    def patch(self, req, pk):
        """
        Customer: Edit the quantity of an order.
        """
        input_serializer = InputBuySerializer(data=req.data)
        input_serializer.is_valid(raise_exception=True)
        order = edit_order(quantity=input_serializer.validated_data['quantity'], pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, req, pk):
        """
        Customer: Delete an order.
        """
        delete_order(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuyAPI(APIView):
    @extend_schema(
        request=EditOrderSerializer,
        responses=OrderSerializer,
    )
    def post(self, req):
        """
        Customer: Add new order to his/her not paid payment.
        """
        input_serializer = EditOrderSerializer(data=req.data)
        input_serializer.is_valid(raise_exception=True)
        order = buy_product(quantity=input_serializer.validated_data['quantity'],
                            product_pk=input_serializer.validated_data['product_pk'], user=req.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
