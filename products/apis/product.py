from rest_framework.views import APIView
from products.serializers import ProductSerializer, EditCreateProductSerializer
from products.services import search_list, get_category, create_product, get_product, edit_product, delete_product, \
    get_all_products
from rest_framework.response import Response
from rest_framework import status


class ProductApi(APIView):
    def get(self, req):
        """
        Customer: View list of all products.
        """
        products = get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductAccountApi(APIView):
    def get(self, req):
        """
        Seller: View list of seller's products.
        """
        products = search_list(data={'user': req.user})
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        """
        Seller: Creates new product.
        """
        input_serializer = EditCreateProductSerializer(data=req.data)
        input_serializer.is_valid(raise_exception=True)
        category = get_category(pk=input_serializer.validated_data['category'])
        product = create_product(name=input_serializer.validated_data['name'],
                                 price=input_serializer.validated_data['price'], category=category,
                                 discount=input_serializer.validated_data['discount'], user=req.user)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDeleteProductApi(APIView):
    def get(self, req, pk):
        """
        Seller/Customer: Retrieve a product.
        """
        product = get_product(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, pk):
        """
        Seller: Edit a product.
        """
        input_serializer = EditCreateProductSerializer(data=req.data)
        input_serializer.is_valid(raise_exception=True)
        category = get_category(pk=input_serializer.validated_data['category'])
        product = edit_product(name=input_serializer.validated_data['name'],
                               price=input_serializer.validated_data['price'], category=category,
                               discount=input_serializer.validated_data['discount'], pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, req, pk):
        """
        Seller: Delete a product.
        """
        delete_product(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
