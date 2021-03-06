"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Order, Product, OrderProduct, Customer, PaymentType


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Orders

    Arguments:
        serializers
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product')
        depth = 1

class OrderProducts(ViewSet):
    """Orders for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Order instance
        """
        new_order_product = OrderProduct()
        order = Order.objects.get(pk=request.data["order_id"])
        product = Product.objects.get(pk=request.data["product_id"])

        new_order_product.order = order
        new_order_product.product = product
        new_order_product.save()

        serializer = OrderProductSerializer(new_order_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(orderproduct, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an Order

        Returns:
            Response -- Empty body with 204 status code
        """
        order_product = OrderProduct.objects.get(pk=pk)
        order = Order.objects.get(pk=request.data["order_id"])
        product = Product.objects.get(pk=request.data["product_id"])

        order_product.order = order
        order_product.product = product
        order_product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
            how to get current users open order
        """
        try:

            orderproduct = OrderProduct.objects.get(pk=pk)
            orderproduct.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        order_products = OrderProduct.objects.all()

        order = self.request.query_params.get('order', None)
        product = self.request.query_params.get('product', None)
        payment = self.request.query_params.get('payment', None)


        if product is not None:
            order_products = order_products.filter(product__id=product)
        if order is not None:
            order_products = order_products.filter(order_payment=None)

        serializer = OrderProductSerializer(
            order_products, many=True, context={'request': request})
        return Response(serializer.data)
