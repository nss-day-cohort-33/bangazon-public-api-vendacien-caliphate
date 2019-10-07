"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Order, Customer, PaymentType, OrderProduct


class OrderSerializer(serializers.HyperlinkedModelSerializer):
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
        fields = ('id', 'url', 'customer_id', 'paymenttype_id')


class Orders(ViewSet):
    """Orders for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Order instance
        """
        new_order = OrderProduct()
        new_order.created_at = request.data["created_at"]
        customer = Customer.objects.get(pk=request.data["customer_id"])
        paymenttype = PaymentType.objects.get(pk=request.data["paymenttype_id"])

        new_order.paymenttype = paymenttype
        new_order.customer = customer
        new_order.save()

        serializer = OrderSerializer(new_order, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            customer = Order.objects.get(pk=pk)
            paymenttype = Order.objects.get(pk=pk)
            serializer = OrderSerializer(customer, paymenttype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an Order

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.created_at = request.data["created_at"]
        customer = Customer.objects.get(pk=request.data["customer_id"])
        paymenttype = PaymentType.objects.get(pk=request.data["paymenttype_id"])

        order.customer = customer
        order.paymenttype = paymenttype
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            customer = Order.objects.get(pk=pk)
            paymenttype = Order.objects.get(pk=pk)
            customer.delete()
            paymenttype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        orders = Order.objects.all()

        # Support filtering Orders by customer id
        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            orders = orders.filter(customer__id=customer)

        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)


# description - This is the view for Orders, where the http request are defined for Orders
# Author - Drew Palazola
# properties -
# 1. Order serializers
# 2. Create
# 3.Retrieve
# 4.Update
# 5.Destroy
# 6.List