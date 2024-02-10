from django.contrib import admin
from data.models import FeatureCollection, RasterLayer, VectorLayer

class FeatureCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vectorlayer_name')

    def vectorlayer_name(self, obj):
        return obj.vectorlayer.name if obj.vectorlayer else ""

admin.site.register(VectorLayer)
admin.site.register(RasterLayer)
admin.site.register(FeatureCollection, FeatureCollectionAdmin)
