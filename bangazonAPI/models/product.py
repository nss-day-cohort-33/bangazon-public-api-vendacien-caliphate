from django.db import models
from django.urls import reverse
from .producttype import ProductType
from .customer import Customer

class Product(models.Model):
    '''
    description: This class creates a Product and its properties and joins it to Customer and Product Type.
    author: Group Code
    properties:
      name: product title
      customer: foreign key of customer id
      price: price of the product as an integer
      description: description of the product
      quantity: number of product available
      created_at: date of creation
      producttype: foreign key of producttype id
      city: city the product is available in to be sold
      product_image: path for user uploading product images to product
    '''

    name = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    producttype = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='bangazon-public-api-vendacien-caliphate/BangazonProject/bangazonAPI/product_image')
    


    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"pk": self.pk})

