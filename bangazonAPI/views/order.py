"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Order, Customer, PaymentType, OrderProduct, Product
from .orderproduct import OrderProductSerializer
from .product import ProductSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
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
        fields = ('id', 'url', 'product', 'paymenttype', 'customer')
        depth = 1

class Orders(ViewSet):
    """Orders for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Order instance
        """
        order_item = OrderProduct()
        order_item.product = Product.objects.get(pk=request.data["product_id"])

        order = Order.objects.filter(customer=request.auth.user, paymenttype__isnull=False)
        current_customer = Customer.objects.get(customer=request.auth.user)

        if order.exists():
            print("open order in db. Add it and the prod to OrderProduct")
            order_item.order = order[0]
        else:
            print("no open orders. Time to make a new order to add this product to")
            new_order = Order()
            new_order.customer = current_customer
            new_order.save()
            order_item.order = new_order

        order_item.save()

        serializer = OrderProductSerializer(order_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an Order

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        payment = PaymentType.objects.get(pk=request.data["payment_id"])
        order.payment = payment
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

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
        customer = Customer.objects.get(pk=1)
        # (pk=request.auth.user)

        cart = self.request.query_params.get('cart', None)
        orders = orders.filter(customer=customer)
        print("orders", orders)
        if cart is not None:
            orders = orders.filter(paymenttype=None).get()
            print("orders filtered", orders)
            serializer = OrderSerializer(
                orders, many=False, context={'request': request}
            )

        else:
            serializer = OrderSerializer(
                orders, many=True, context={'request': request}
            )
        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)