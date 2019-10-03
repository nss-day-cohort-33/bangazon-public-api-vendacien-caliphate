from django.db import models

class ProductType(models.Model):
    """
    Creates the table for product type
    Author: Group Code
    methods: none

    name: title of product type
    """

    name = models.CharField(max_length=55)