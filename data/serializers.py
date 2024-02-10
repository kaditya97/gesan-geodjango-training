from rest_framework import serializers
from data.models import (
    VectorLayer,
    RasterLayer,
)

class VectorLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorLayer
        exclude = ("file",)

class VectorLayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorLayer
        exclude = ("geometry_type", "bbox")

class VectorLayerPatchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = VectorLayer
        exclude = ("file", "geometry_type", "bbox")

class RasterLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasterLayer
        exclude = ("file", "sld")

class RasterLayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasterLayer
        exclude = ("bbox",)

class RasterLayerPatchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = RasterLayer
        exclude = ("file", "sld", "bbox")
