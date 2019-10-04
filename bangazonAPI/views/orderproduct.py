"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Order, Product, OrderProduct


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Orders

    Arguments:
        serializers
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'order_id', 'product_id')


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
            order = OrderProduct.objects.get(pk=pk)
            product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order, product, context={'request': request})
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
        """
        try:
            order = OrderProduct.objects.get(pk=pk)
            product = OrderProduct.objects.get(pk=pk)
            order.delete()
            product.delete()

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

        # Support filtering OrderProduct by Order id
        order = self.request.query_params.get('order', None)
        if order is not None:
            order_products = order_products.filter(order__id=order)

        serializer = OrderProductSerializer(
            order_products, many=True, context={'request': request})
        return Response(serializer.data)

# description - This is the view for OrderProduct, where the http request are defined for OrderProducts
# Author - Drew Palazola
# properties -
# 1. Order serializers
# 2. Create
# 3.Retrieve
# 4.Update
# 5.Destroy
# 6.List