import geopandas as gpd
import rasterio
from rasterio import features
import numpy as np
"""
This code calls in the shapefile of the lakes and converts it to a raster (.tif) file
The Avalanche.tif file is used as a guide raster to snap to.
The value of each lake is in the output raster is the unique lake ID. 
"""
# Paths to your shapefile and DEM raster
shapefile_path = r"/media/snowman/LaCie/cascading_slushflow/fonnbu/Fonnbu_lakes.shp"
dem_raster_path = r"/media/snowman/LaCie/cascading_slushflow/fonnbu/fonnbu_avalanche.tif"
output_raster_path = r"/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster1.tif"

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
resampled_data = np.zeros((1, dem_shape[0], dem_shape[1]), dtype='uint32')

with rasterio.open(output_raster_path, 'w', **output_profile) as dst:
    for idx, lake_id in enumerate(gdf['FID'].unique(), start=1):
        # Select polygons for the current lake ID
        subset_gdf = gdf[gdf['FID'] == lake_id]

        # Create a mask for the current lake
        mask = features.geometry_mask(subset_gdf['geometry'], out_shape=dem_shape, transform=dem_transform, invert=True)

        # Accumulate the pixels corresponding to the lake with the lake's unique ID
        resampled_data += np.where(mask, lake_id, 0).astype('uint32')

    # Remove the singleton dimension from the front of the array
    resampled_data = resampled_data.squeeze()

    # Write the accumulated data to the output raster
    dst.write(resampled_data, 1)

print("Output raster created successfully at:", output_raster_path)
