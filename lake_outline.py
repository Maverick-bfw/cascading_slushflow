import rasterio
from rasterio.windows import Window
import numpy as np

def get_lowest_neighbor_elevation(dem, mask):
    # Define a neighborhood window (e.g., 3x3)
    neighborhood = np.ones((3, 3))

    # Mask the DEM with the neighborhood
    dem_masked = np.where(mask, dem, np.nan)

    # Find the minimum elevation in the neighborhood
    lowest_neighbor_elevation = np.nanmin(dem_masked)

    return lowest_neighbor_elevation

# Paths to input and output raster files
dem_files = [
    "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6801_4_10m_z33.tif",
    "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6800_1_10m_z33.tif"
]
lake_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster.tif"
output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/lowest_elevation_around_lake.tif"

# Open lake raster file
with rasterio.open(lake_file) as lake_src:
    # Read lake raster data
    lake = lake_src.read(1)
    profile = lake_src.profile  # Get profile from lake raster for output raster

    # Initialize a new array for the output raster with NoData values
    output_data = np.full_like(lake, fill_value=profile["nodata"], dtype=profile["dtype"])

    # Get the coordinates of lake cells
    lake_cells = np.where(lake == 1)

    # Read data from each DEM file
    for dem_file in dem_files:
        with rasterio.open(dem_file) as dem_src:
            # Iterate over each lake cell
            for y, x in zip(*lake_cells):
                # Define the window around the lake cell
                window = Window(x - 1, y - 1, 3, 3)

                # Read the neighborhood values from the DEM
                neighborhood_dem = dem_src.read(1, window=window)

                # Create a mask for the neighborhood to avoid nodata values
                neighborhood_mask = neighborhood_dem != dem_src.nodata

                # Get the lowest elevation value in the neighborhood
                lowest_elevation = get_lowest_neighbor_elevation(neighborhood_dem, neighborhood_mask)

                # Set the lowest elevation value in the output raster
                output_data[y, x] = lowest_elevation

# Update profile to match lake raster profile
profile.update(dtype=profile["dtype"], count=1)

# Write the output raster
with rasterio.open(output_file, "w", **profile) as dst:
    dst.write(output_data, 1)
