from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
<<<<<<< HEAD
from bangazonAPI import models
=======
from bangazonAPI.models import *
>>>>>>> 63d09e35eb778c01657cc0dc7a07acf24e4dc78f

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]