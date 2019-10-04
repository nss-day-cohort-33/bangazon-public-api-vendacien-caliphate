from django.db import models
from .customer import Customer
from .paymenttype import PaymentType

class Order(models.Model):
    """
    Creates the join table for the many to many relationship between paymenttype and customer
    Author: Group Code
    methods: none
    """

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    paymenttype = models.ForeignKey("PaymentType", on_delete=models.CASCADE)
    created_at = models.DateTimeField()