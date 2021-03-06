from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonAPI.models import *
from bangazonAPI.views import Products
from bangazonAPI.views import ProductTypes
from bangazonAPI.views import Orders
from bangazonAPI.views import OrderProducts
from bangazonAPI.views import Customers
from bangazonAPI.views import PaymentTypes
from bangazonAPI.views import register_user, login_user
from bangazonAPI.views import ProductCategories, UserViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', Products, 'product')
router.register(r'producttypes', ProductTypes, 'producttype')
router.register(r'orders', Orders, 'order')
router.register(r'orderproducts', OrderProducts, 'orderproduct')
router.register(r'customers', Customers, 'customer')
router.register(r'users', UserViewSet, 'user')
router.register(r'products', Products, 'product')
router.register(r'paymenttypes', PaymentTypes, 'paymenttype')
router.register(r'productcategories', ProductCategories, 'productcategory')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]