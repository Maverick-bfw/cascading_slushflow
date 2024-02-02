import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.transform import from_origin
from rasterio.enums import Resampling
import numpy as np
"""
This code reads in Fonnbus lake shape file and transforms it into a Raster.tif file. 
The lake ID "FID" is saved in the raster cells so each lake can be picked out easy with a loop in the next processing steps
The dem_raster_path is not a dem but the Flow-py avalnche layer and was used to get a raster to snap to. 
"""
# Paths to your shapefile and DEM raster
shapefile_path = r"D:\cascading_slushflow\fonnbu\Fonnbu_lakes.shp"
dem_raster_path = r"D:\cascading_slushflow\fonnbu\fonnbu_avalanche.tif"
output_raster_path = r"D:\cascading_slushflow\fonnbu\output_lakes_raster.tif"

# Read the shapefile
gdf = gpd.read_file(shapefile_path)

# Open the DEM raster to get its properties
with rasterio.open(dem_raster_path) as dem_src:
    dem_profile = dem_src.profile
    dem_transform = dem_src.transform
    dem_crs = dem_src.crs
    dem_shape = dem_src.shape

# Create a blank raster with a single band
output_profile = dem_profile.copy()
output_profile.update(count=1, dtype='uint32')  # Assuming unique IDs are integers

# Use an in-memory raster to store the resampled data
resampled_data = np.empty((1, dem_shape[0], dem_shape[1]), dtype='uint32')

with rasterio.open(output_raster_path, 'w', **output_profile) as dst:
    for idx, lake_id in enumerate(gdf['FID'].unique(), start=1):
        # Select polygons for the current lake ID
        subset_gdf = gdf[gdf['FID'] == lake_id]

        # Create a mask for the current lake
        mask = features.geometry_mask(subset_gdf['geometry'], out_shape=dem_shape, transform=dem_transform, invert=True)

        # Set the pixels corresponding to the lake to the lake's unique ID
        dst.write(np.where(mask, lake_id, dst.nodata), 1)

    # Optionally, resample the output raster
    rasterio.warp.reproject(dst.read(1), resampled_data, src_transform=dem_transform, dst_transform=dem_transform,
                            src_crs=dem_crs, dst_crs=dem_crs, resampling=Resampling.nearest)

# Write the resampled data to the output raster
with rasterio.open(output_raster_path, 'r+') as dst:
    dst.write(resampled_data)



"""
# OLD VERSION OF CODE
from osgeo import gdal, ogr, osr
from pathlib import Path

# Paths to the input files
#file_path = Path("/home/chris/OneDrive/cascading_slushflow/") # linux path
file_path = Path("C:/Users/cda055/OneDrive - UiT Office 365/cascading_slushflow/") # windows path
lakes_shapefile_path = file_path / Path("lakes/NVEData/Innsjo/Innsjo_Innsjo.shp")
avalanche_raster_path = file_path / Path("Flow-py_18deg_avalanche/flow-py-norway_travel_angle_18.tif")
output_raster_path = file_path / "output_rasterized_lakes.tif"

# Open the avalanche raster to get its properties
gdal.SetConfigOption('GTIFF_SRS_SOURCE', 'EPSG')

avalanche_ds = gdal.Open(str(avalanche_raster_path))
avalanche_band = avalanche_ds.GetRasterBand(1)
avalanche_gt = avalanche_ds.GetGeoTransform()
projection = avalanche_ds.GetProjection()

# Get the extent and resolution from the avalanche raster
xmin, ymax, xmax, ymin = avalanche_gt[0], avalanche_gt[3], avalanche_gt[0] + avalanche_ds.RasterXSize * avalanche_gt[1], avalanche_gt[3] - avalanche_ds.RasterYSize * avalanche_gt[5]
pixel_size_x = avalanche_gt[1]
pixel_size_y = avalanche_gt[5]
x_res = avalanche_ds.RasterXSize
y_res = avalanche_ds.RasterYSize

# Create a blank raster to burn the lakes into
target_ds = gdal.GetDriverByName('GTiff').Create(str(output_raster_path), x_res, y_res, 1, gdal.GDT_Byte)
target_ds.SetGeoTransform((xmin, pixel_size_x, 0, ymax, 0, pixel_size_y))
target_ds.SetProjection(projection)
band = target_ds.GetRasterBand(1)
band.SetNoDataValue(0)

# Open the lakes shapefile
lakes_ds = ogr.Open(str(lakes_shapefile_path))
lakes_layer = lakes_ds.GetLayer()

# Rasterize the lakes onto the blank raster
gdal.RasterizeLayer(target_ds, [1], lakes_layer, burn_values=[1])

# Close the datasets
target_ds = None
lakes_ds = None
avalanche_ds = None
"""