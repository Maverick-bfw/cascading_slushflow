import rasterio

"""
This code reads in two raster files and makes sure they are 
the same resolution, extent and snapped to each other.
"""
def check_raster_properties(raster_path):
    with rasterio.open(raster_path) as src:
        resolution = src.res
        extent = src.bounds
        transform = src.transform

    return resolution, extent, transform

# Paths to the raster files
lakes_raster_path = r"/media/snowman/LaCie/cascading_slushflow/fonnbu/fonnbu_lakes.tif"
avalanche_raster_path = r"/media/snowman/LaCie/cascading_slushflow/fonnbu/Fonnbu_avalanche.tif"

# Check properties of the lakes raster
lakes_resolution, lakes_extent, lakes_transform = check_raster_properties(lakes_raster_path)

# Check properties of the avalanche raster
avalanche_resolution, avalanche_extent, avalanche_transform = check_raster_properties(avalanche_raster_path)

# Compare properties
if lakes_resolution == avalanche_resolution:
    print("The lakes and avalanche rasters have the same resolution.")
else:
    print("The lakes and avalanche rasters have different resolutions.")

if lakes_extent == avalanche_extent:
    print("The lakes and avalanche rasters have the same extent.")
else:
    print("The lakes and avalanche rasters have different extents.")

if lakes_transform == avalanche_transform:
    print("The lakes and avalanche rasters are snapped to each other.")
else:
    print("The lakes and avalanche rasters are not snapped to each other.")
