from django.db import models
from django.urls import reverse
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class PaymentType(SafeDeleteModel):
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
    _safedelete_policy = SOFT_DELETE
    merchant_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25)
    exp_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("PaymentType")
        verbose_name_plural = ("PaymentTypes")

    def get_absolute_url(self):
        return reverse("paymenttype_details", kwargs={"pk": self.pk})