import rasterio
import numpy as np
from rasterio.features import geometry_mask

file_path = "/home/chris/OneDrive/cascading_slushflow/"
lakes_path = file_path + "lakes/raster_lakes.tif"
avalanche_path = file_path + "Flow-py_18deg_avalanche/flow-py-norway_travel_angle_18.tif"

# Read the rasterized lake layer
with rasterio.open(lakes_path) as lakes_raster:
    lakes_data = lakes_raster.read(1)

# Open the avalanche raster
with rasterio.open(avalanche_path) as avalanche_area:
    avalanche_data = avalanche_area.read(1)

# Count overlapping cells between the two rasters
overlap_count = np.sum((avalanche_data > 0) & (lakes_data > 0))

# Set the threshold for significant overlap
overlap_threshold = 2  # Adjust as needed

# Check if the overlap count meets the threshold
if overlap_count >= overlap_threshold:
    print(f"There are {overlap_count} cells with significant overlap between lakes and avalanche areas.")
else:
    print("The overlap between lakes and avalanche areas is below the threshold.")
