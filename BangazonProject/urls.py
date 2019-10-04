from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonAPI.models import *
from bangazonAPI.views import Products
from bangazonAPI.views import ProductTypes
from bangazonAPI.views import Customers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', Products, 'product')
router.register(r'producttypes', ProductTypes, 'producttype')


router.register(r'customers', Customers, 'customer')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]