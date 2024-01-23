from osgeo import gdal
import rasterio
from rasterio.windows import Window
import numpy as np
import pickle
from pathlib import Path

# Paths to the input files
#file_path = Path("/home/chris/OneDrive/cascading_slushflow/") # linux path
file_path = Path("C:/Users/cda055/OneDrive - UiT Office 365/cascading_slushflow/") # windows path

avalanche_raster_path = file_path / Path("Flow-py_18deg_avalanche/flow-py-norway_travel_angle_18.tif")
lakes_raster_path = file_path / "output_rasterized_lakes.tif"


output_updated_raster_path = file_path / "fonnbu_union_result.tif"


# Open the lakes raster
with rasterio.open(str(lakes_raster_path)) as lakes_raster:
    # Read the lakes raster data as a NumPy array
    lakes_data = lakes_raster.read(1)

    # Open the avalanche raster
    with rasterio.open(str(avalanche_raster_path)) as avalanche_raster:
        # Read the avalanche raster data as a NumPy array
        avalanche_data = avalanche_raster.read(1)

        # Perform intersection (logical AND) between the arrays
        result_data = np.logical_and(lakes_data > 0, avalanche_data > 0).astype(np.uint8)

        # Create metadata for the output raster using information from the avalanche raster
        meta = avalanche_raster.meta.copy()
        meta.update({'dtype': 'uint8'})

        # Write the result data to a new GeoTIFF file
        with rasterio.open(str(output_updated_raster_path), 'w', **meta) as output_raster:
            output_raster.write(result_data, 1)