from django.db import models
from django.urls import reverse
from .producttype import ProductType
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Product(SafeDeleteModel):
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
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    producttype = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='bangazon-public-api-vendacien-caliphate/BangazonProject/bangazonAPI/product_image')



    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"pk": self.pk})

    @property
    def total_sold(self):
        return self.cart.filter(order__paymenttype__isnull=False).count()

