from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]