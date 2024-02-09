import rasterio
import numpy as np

"""
This code calls in the lakes and avalanche runout rasters 
The spatial intersection between them in calculated and saved in the output raster.
The value of the output raster is the unique lake ID
"""
# Paths to the raster files
lakes_raster_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster.tif"
avalanche_raster_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/Fonnbu_avalanche.tif"
output_raster_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_combined.tif"

# Open the lakes raster to get its properties
with rasterio.open(lakes_raster_path) as lakes_src:
    lakes_data = lakes_src.read(1)
    lakes_transform = lakes_src.transform
    lakes_profile = lakes_src.profile

# Open the avalanche raster to get its properties
with rasterio.open(avalanche_raster_path) as avalanche_src:
    avalanche_data = avalanche_src.read(1)
    avalanche_transform = avalanche_src.transform

# Create an output raster with the same extent and resolution as the lakes raster
with rasterio.open(output_raster_path, 'w', **lakes_profile) as dst:
    # Read the lakes data (Note: This line has been removed)
    # lakes_data = lakes_src.read(1)

    # Create a mask where both avalanche and lakes raster are greater than 0
    mask = np.logical_and(avalanche_data > 0, lakes_data > 0)

    # Set values in the output raster based on the conditions
    combined_data = np.where(mask, lakes_data, 0)

    # Write the data to the output raster
    dst.write(combined_data, 1)

print("Output raster created successfully at:", output_raster_path)
