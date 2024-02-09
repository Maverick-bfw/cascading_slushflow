import rasterio
from rasterio.features import geometry_mask
import numpy as np
from osgeo import gdal
import rasterio
from rasterio.features import shapes
from scipy import ndimage


file_path = "/home/chris/OneDrive/cascading_slushflow/lakes/fonnbu/"

# Paths to input files
lakes_raster_path = file_path + "fonnbu_lakes.tif"
union_raster =file_path + "fonnbu_union_result.tif"


# Open the lakes and union rasters
with rasterio.open(lakes_raster_path) as src_lakes, rasterio.open(union_raster) as src_union:
    # Read raster data as arrays
    lakes = src_lakes.read(1)
    union = src_union.read(1)

    # Find connected regions in lakes raster
    labeled_lakes, num_features = ndimage.label(lakes == 1)

    # Loop through each labeled region
    for i in range(1, num_features + 1):
        # Create a mask for the current lake region
        mask = labeled_lakes == i

        # Check if any cell in the current lake region overlaps with the union raster
        overlap = np.any((mask == 1) & (union == 1))

        # If there's an overlap, count the cells and update the lakes array
        if overlap:
            count = np.sum(mask)
            lakes[mask] = count

    # Write the results to a new raster
    profile = src_lakes.profile
with rasterio.open(file_path + 'result_lake_overlap_count.tif', 'w', **profile) as dst:
    dst.write(lakes, 1)