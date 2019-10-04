"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Product, Customer, ProductType


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'customer_id', 'producttype_id')


class Products(ViewSet):
    """Products for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_product = Product()
        new_product.name = request.data["name"]
        customer = Customer.objects.get(pk=request.data["customer_id"])
        new_product.price = request.data["price"]
        new_product.description = request.data["description"]
        new_product.quantity = request.data["quantity"]
        new_product.created_at = request.data["created_at"]
        producttype = ProductType.objects.get(pk=request.data["producttype_id"])
        new_product.city = request.data["city"]
        new_product.product_image = request.data["product_image"]

        new_product.producttype = producttype
        new_product.customer = customer
        new_product.save()

        serializer = ProductSerializer(new_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            customer = Product.objects.get(pk=pk)
            producttype = Product.objects.get(pk=pk)
            serializer = ProductSerializer(customer, producttype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        customer = Customer.objects.get(pk=request.data["customer_id"])
        product.price = request.data["price"]
        product.description = request.data["description"]
        product.quantity = request.data["quantity"]
        product.created_at = request.data["created_at"]
        producttype = ProductType.objects.get(pk=request.data["producttype_id"])
        product.city = request.data["city"]
        product.product_image = request.data["product_image"]

        product.customer = customer
        product.producttype = producttype
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            customer = Product.objects.get(pk=pk)
            producttype = Product.objects.get(pk=pk)
            customer.delete()
            producttype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        products = Product.objects.all()

        # Support filtering Products by producttype id
        producttype = self.request.query_params.get('producttype', None)
        if producttype is not None:
            products = products.filter(producttype__id=producttype)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)