from django.contrib.gis.db import models

class VectorLayer(models.Model):
    name = models.CharField(max_length=255)
    detail = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to="vectorlayer", null=True, blank=True
    )
    geometry_type = models.CharField(max_length=250, null=True, blank=True)
    bbox = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return self.name
    
class FeatureCollection(models.Model):
    vectorlayer = models.ForeignKey(
        VectorLayer,
        on_delete=models.CASCADE,
        related_name="vectorlayer",
        blank=True,
        null=True,
    )
    attr_data = models.JSONField(default=dict)
    geom = models.GeometryField(srid=4326, blank=True, null=True)

    def __str__(self):
        return self.vectorlayer.name if self.vectorlayer else str(self.pk)
    
class RasterLayer(models.Model):
    name = models.CharField(max_length=255)
    detail = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to="rasterlayer", null=True, blank=True
    )
    sld = models.FileField(upload_to="sld", null=True, blank=True)
    bbox = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return self.name