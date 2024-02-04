import os
from tempfile import NamedTemporaryFile
from osgeo import gdal
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.prototypes.io import wkt_w
from geo.Geoserver import Geoserver
import geopandas as gpd
from rest_framework.response import Response
from rest_framework import status

from data.models import VectorLayer, FeatureCollection, RasterLayer

geo = Geoserver(service_url=settings.GEOSERVER_URL, username=settings.GEOSERVER_USER, password=settings.GEOSERVER_PASSWORD)
print(geo.get_workspace("gesan"))

def get_file_extension(file_upload):
    split_tup = os.path.splitext(file_upload)
    file_extension = split_tup[1]
    return file_extension

def handleFile(file, layer_id, feature_collection_model):
    gdf = gpd.read_file(file)
    geometry_type = gdf["geometry"].iloc[0].geom_type
    total_bounds = gdf.total_bounds
    bound_dict = {"total_bounds": total_bounds.tolist()}
    for index, row in gdf.iterrows():
        dropped_geometry = row.drop(["geometry"])
        dropped_geometry_dict = dropped_geometry.to_dict()
        geom = GEOSGeometry(str(row["geometry"]))
        wkt = wkt_w(dim=2).write(geom).decode()
        geom = GEOSGeometry(wkt)
        feature_collection_model.objects.create(
            vectorlayer_id=layer_id, attr_data=dropped_geometry_dict, geom=geom
        )
    return geometry_type, bound_dict

def upload_vector_layer(id):
    instance = VectorLayer.objects.get(id=id)
    file_extension = get_file_extension(instance.file.path)
    if file_extension == ".zip" or file_extension == ".geojson":
        geometry_type, bound_dict = handleFile(
            instance.file.path, id, FeatureCollection
        )
        instance.geometry_type = geometry_type
        instance.bbox = bound_dict
        instance.save()
    else:
        instance.delete()
        return Response("File format not supported", status=status.HTTP_400_BAD_REQUEST)

    
def upload_raster_layer(id):
    instance = RasterLayer.objects.get(id=id)
    workspace_name = settings.GEOSERVER_RASTER_WORKSPACE
    file_extension = get_file_extension(instance.file.path)
    if file_extension == ".tif":
        try:
            workspace = geo.get_workspace(workspace_name)
            if not workspace:
                geo.create_workspace(workspace_name)
            layer_path = instance.file.path
            layer_name = os.path.basename(layer_path).split(".")[0]
            geo.create_coveragestore(
                layer_name=layer_name,
                path=instance.file.path,
                workspace=workspace_name,
            )
            if instance.sld is not None:
                sld_file_path = instance.sld.path
                sld_name = os.path.basename(sld_file_path).split(".")[0]
                geo.upload_style(
                    path=sld_file_path,
                    workspace=workspace_name,
                )
                geo.publish_style(
                    layer_name=layer_name,
                    style_name=sld_name,
                    workspace=workspace_name,
                )
            with NamedTemporaryFile(suffix=".tif") as tmp:
                gdal.Warp(tmp.name, layer_path, dstSRS="EPSG:4326")
                ds = gdal.Open(tmp.name)
                width = ds.RasterXSize
                height = ds.RasterYSize
                geotransform = ds.GetGeoTransform()
                extent = [
                    geotransform[0],
                    geotransform[3] + height * geotransform[5],
                    geotransform[0] + width * geotransform[1],
                    geotransform[3],
                ]
                instance.bbox = extent
                instance.save()
                tmp.close()
        except Exception as e:
            instance.delete()
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    else:
        instance.delete()
        return Response("File format not supported", status=status.HTTP_400_BAD_REQUEST)
        
    
