from rest_framework import serializers
from .models import Product, Order, Payment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'seller', 'discount']


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


class InputBuySerializer(serializers.Serializer):
    quantity = serializers.IntegerField()


class EditOrderSerializer(serializers.Serializer):
    product_pk = serializers.IntegerField()
    quantity = serializers.IntegerField()


class EditCreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    category = serializers.IntegerField()
    price = serializers.IntegerField()
    discount = serializers.IntegerField(default=0, required=False)

    def validate_name(self, name):
        if name.isnumeric():
            raise serializers.ValidationError('The name must be string')
        else:
            return name
