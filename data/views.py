from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from data.models import VectorLayer, RasterLayer
from data.serializers import (
    VectorLayerSerializer,
    VectorLayerPostSerializer,
    VectorLayerPatchSerializer,
    RasterLayerSerializer,
    RasterLayerPostSerializer,
    RasterLayerPatchSerializer,
)
from data.utils import upload_vector_layer, upload_raster_layer

# *****************Pagination******************
class LayerlistPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
# *****************Pagination******************

# Create your views here.
class VectorViewSet(ModelViewSet):
    queryset = VectorLayer.objects.all()
    serializer_class = VectorLayerSerializer
    pagination_class = LayerlistPagination
    parser_classes = (FormParser, MultiPartParser)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ["name", "geometry_type"]
    ordering_fields = ["id", "name"]
    serializer_classes = {
        "create": VectorLayerPostSerializer,
        "partial_update": VectorLayerPatchSerializer,
    }

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [permissions.IsAuthenticated()]
        else:
            return super().get_permissions()
        
    def get_serializer_class(self):
        """
        Get the appropriate serializer class based on the request action.
        Returns the serializer class for the given request action.
        """
        return self.serializer_classes.get(self.action, self.serializer_class)
    
    def create(self, request, **kwargs):
        """
        Upload Vector Data
        Supported Formats: Shapefile(zipped), Geojson
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            try:
                upload_vector_layer(instance.id)
            except:
                instance.delete()
                return Response("Error parsing file", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class RasterViewSet(ModelViewSet):
    queryset = RasterLayer.objects.all()
    serializer_class = RasterLayerSerializer
    pagination_class = LayerlistPagination
    parser_classes = (FormParser, MultiPartParser)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    serializer_classes = {
        "create": RasterLayerPostSerializer,
        "partial_update": RasterLayerPatchSerializer,
    }

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [permissions.IsAuthenticated()]
        else:
            return super().get_permissions()
        
    def get_serializer_class(self):
        """
        Get the appropriate serializer class based on the request action.
        Returns the serializer class for the given request action.
        """
        return self.serializer_classes.get(self.action, self.serializer_class)
    
    def create(self, request, **kwargs):
        """
        Upload Raster Data
        Supported Formats: Tiff
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            try:
                upload_raster_layer(instance.id)
            except:
                instance.delete()
                return Response("Error parsing file", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    