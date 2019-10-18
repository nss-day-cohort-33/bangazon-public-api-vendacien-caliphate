"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Product, Customer, ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class ProductTypes(ViewSet):
    """Products for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_product_type = ProductType()
        new_product_type.name = request.data["name"]
        new_product_type.save()

        serializer = ProductTypeSerializer(new_product_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            serializer = ProductTypeSerializer(context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        product_type = ProductType.objects.get(pk=pk)
        product_type.name = request.data["name"]
        product_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:


            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        product_types = ProductType.objects.all()

        # Support filtering attractions by area id
        name = self.request.query_params.get('name', None)
        if name is not None:
            product_types = product_types.filter(name__id=name)

        serializer = ProductTypeSerializer(
            product_types, many=True, context={'request': request})
        return Response(serializer.data)