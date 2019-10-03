from django.db import models
from django.urls import reverse
from .customer import Customer

class PaymentType(models.Model):
    '''
    description: This class creates a Payment Type and its properties and joins it to Customer.
    author: Group Code
    properties:
      merchant_name: name of merchant
      account_number: merchant's payment account number
      exp_date: merchants payment expiration date
      customer: foreign key for customer id from customer
      created_at: date of creation of payment type
    '''

    merchant_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25)
    exp_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


    class Meta:
        verbose_name = ("PaymentType")
        verbose_name_plural = ("PaymentTypes")

    def get_absolute_url(self):
        return reverse("paymenttype_details", kwargs={"pk": self.pk})