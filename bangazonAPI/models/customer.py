from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
    '''
    description: This class creates a customer and its properties
    author: Group Code
    properties:
      first_name: customer first name
      last_name: customer last name
      email: customer email address
      date_joined: the date of customer account creation
      isActive: boolean to list if the customer account is active or not
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    # class Meta:
    #     ordering = (F('user.date_joined').asc(nulls_last=True),)