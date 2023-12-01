#from osgeo import gdal, osr
import numpy as np
import os
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from shapely.geometry import mapping

file_path = "/home/chris/OneDrive/cascading_slushflow/"
lakes_path = file_path + "lakes/raster_lakes.tif"
avalanche_path = file_path + "Flow-py_18deg_avalanche/flow-py-norway_travel_angle_18.tif"
output_path = file_path + "union_result.tif"

# Open the target raster dataset to get its extent
#avalanche_area = gdal.Open(avalanche_path, gdal.GA_ReadOnly)
#if avalanche_area is None:
#    print("Failed to open the target raster dataset.")
#    exit(1)

# Open the raster file
with rasterio.open(avalanche_path) as avalanche_area:
    disaster_area = avalanche_area.read(1)  # Read the raster band
    # Get metadata for the raster
    src_meta = avalanche_area.meta.copy()
    src_crs = avalanche_area.crs

# Open the shape file
lakes = gpd.read_file(lakes_path)

# Perform spatial intersection between disaster area and lakes
intersection = gpd.overlay(lakes, avalanche_area, how='intersection')

# Create a new raster representing the intersection
# Assuming 'intersection' is a GeoDataFrame with the intersection result
with rasterio.open(output_path, 'w', **src_meta) as out:
    out_arr = out.read(1)
    shapes = [(geom, 1) for geom in intersection.geometry]
    burned = rasterize(shapes, out_shape=out_arr.shape, transform=out.transform)
    out.write_band(1, burned)



"""

# Get the projection info of the target raster
target_projection = target_raster_dataset.GetProjection()
# Create a spatial reference for the target projection
target_srs = osr.SpatialReference()
target_srs.ImportFromWkt(target_projection)

# Get the dimensions of the target raster
target_cols = target_raster_dataset.RasterXSize
target_rows = target_raster_dataset.RasterYSize

# Get the extent (bounding box) of the target raster
target_extent = (
    target_raster_dataset.GetGeoTransform()[0],  # left
    target_raster_dataset.GetGeoTransform()[3] + target_raster_dataset.RasterYSize * target_raster_dataset.GetGeoTransform()[5],  # top
    target_raster_dataset.GetGeoTransform()[0] + target_raster_dataset.RasterXSize * target_raster_dataset.GetGeoTransform()[1],  # right
    target_raster_dataset.GetGeoTransform()[3]  # bottom
)


# Calculate the srcwin parameters
srcwin_params = f"-srcwin {target_extent[0]} {target_extent[1]} {target_cols} {target_rows}"

# Clip the second raster to the extent of the target raster
clipped_second_raster_path = "clipped_second_raster.tif"
# Reproject the second raster to the target projection
reprojected_second_raster_dataset = gdal.Warp(clipped_second_raster_path, second_raster_dataset, dstSRS=target_srs.ExportToWkt())

os.system(f"gdal_translate {srcwin_params} {second_raster_path} {clipped_second_raster_path}")

# Open the clipped second raster dataset
clipped_second_raster_dataset = gdal.Open(clipped_second_raster_path, gdal.GA_ReadOnly)
if clipped_second_raster_dataset is None:
    print("Failed to open the clipped second raster dataset.")
    exit(1)

# Perform element-wise multiplication
# Assuming both rasters have the same dimensions and resolutions
result_array = clipped_second_raster_dataset.ReadAsArray() * target_raster_dataset.ReadAsArray()

# Create a new GeoTIFF for the result
driver = gdal.GetDriverByName('GTiff')
result_dataset = driver.Create(output_path, result_array.shape[1], result_array.shape[0], 1, gdal.GDT_Float32)

# Set the geotransform and projection info
result_dataset.SetGeoTransform(clipped_second_raster_dataset.GetGeoTransform())
result_dataset.SetProjection(clipped_second_raster_dataset.GetProjection())

# Write the result to the output raster band
result_band = result_dataset.GetRasterBand(1)
result_band.WriteArray(result_array)

# Close datasets
result_band = None
result_dataset = None
clipped_second_raster_dataset = None

print("Multiplication completed. Result saved at:", output_path)

# Remove the temporarily clipped second raster file
os.remove(clipped_second_raster_path)
"""