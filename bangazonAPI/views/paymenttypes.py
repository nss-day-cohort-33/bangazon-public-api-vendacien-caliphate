"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import PaymentType, Customer
from datetime import *




class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types
    Author: Jake Scott
    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant_name', 'account_number', 'exp_date', 'customer_id')
        depth = 1


class PaymentTypes(ViewSet):
    """Payment types for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """

        # def check_expiration():
        #     print(datetime.today())
        #     print(datetime.strptime(request.data["exp_date"], '%Y-%m-%d'))
        if datetime.today() <= datetime.strptime(request.data["exp_date"], '%Y-%m-%d'):
            new_paymenttype = PaymentType()
            new_paymenttype.merchant_name = request.data["merchant_name"]
            new_paymenttype.account_number = request.data["account_number"]
            new_paymenttype.exp_date = request.data["exp_date"]
            customer = Customer.objects.get(user=request.auth.user)
            new_paymenttype.customer = customer
            new_paymenttype.save()

            serializer = PaymentTypeSerializer(new_paymenttype, context={'request': request})

            return Response(serializer.data)
        else:
            return Response({"error": "Dat date no good"}, status=status.HTTP_400_BAD_REQUEST)

        # check_expiration()

    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment types

        Returns:
            Response -- JSON serialized payment type instance
        """
        try:
            customer = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a payment types

        Returns:
            Response -- Empty body with 204 status code
        """
        new_paymenttype = PaymentType()
        new_paymenttype.merchant_name = request.data["merchant_name"]
        new_paymenttype.account_number = request.data["account_number"]
        new_paymenttype.exp_date = request.data["exp_date"]
        customer = Customer.objects.get(pk=request.data["customer_id"])
        new_paymenttype.created_at = request.data["created_at"]
        new_paymenttype.customer = customer
        new_paymenttype.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            customer = PaymentType.objects.get(pk=pk)
            customer.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to payment types

        Returns:
            Response -- JSON serialized list of payment types
        """
        paymenttypes = PaymentType.objects.all()

        # Support filtering Products by producttype id
        customer = self.request.query_params.get('customer_id', None)
        if customer is not None:
            paymenttypes = paymenttypes.filter(customer=customer)

        serializer = PaymentTypeSerializer(
            paymenttypes, many=True, context={'request': request})
        return Response(serializer.data)


