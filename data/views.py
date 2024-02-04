from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class VectorViewSet(ModelViewSet):
    queryset = None

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [permissions.IsAuthenticated()]
        else:
            return super().get_permissions()

class RasterViewSet(ModelViewSet):
    queryset = None

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [permissions.IsAuthenticated()]
        else:
            return super().get_permissions()