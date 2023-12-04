import rasterio
from rasterio.windows import Window
import numpy as np
import pickle

file_path = "/home/chris/OneDrive/cascading_slushflow/lakes/fonnbu/"

# Paths to input files
lakes_raster_path = file_path + "fonnbu_lakes.tif"
avalanche_raster_path = file_path + "fonnbu_avalanche.tif"
output_updated_raster_path =file_path + "fonnbu_union_result.tif"


# Open the lakes raster
with rasterio.open(lakes_raster_path) as lakes_raster:
    # Read the lakes raster data as a NumPy array
    lakes_data = lakes_raster.read(1)

    # Open the avalanche raster
    with rasterio.open(avalanche_raster_path) as avalanche_raster:
        # Read the avalanche raster data as a NumPy array
        avalanche_data = avalanche_raster.read(1)

        # Perform intersection (logical AND) between the arrays
        result_data = np.logical_and(lakes_data > 0, avalanche_data > 0).astype(np.uint8)

        # Create metadata for the output raster using information from the avalanche raster
        meta = avalanche_raster.meta.copy()
        meta.update({'dtype': 'uint8'})

        # Write the result data to a new GeoTIFF file
        with rasterio.open(output_updated_raster_path, 'w', **meta) as output_raster:
            output_raster.write(result_data, 1)