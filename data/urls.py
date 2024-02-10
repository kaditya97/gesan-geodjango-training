from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from data.views import RasterViewSet, VectorViewSet

router = routers.DefaultRouter()
router.register("raster", RasterViewSet)
router.register("vector", VectorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]