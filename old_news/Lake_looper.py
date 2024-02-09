import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
import numpy as np

# Define the paths to your shapefile and raster file
shapefile_path = r"D:\cascading_slushflow\National_data\lakes\NVEData\Innsjo\Innsjo_Innsjo.shp"
raster_path = r"D:\cascading_slushflow\fonnbu\fonnbu_avalanche.tif"

# Read the shapefile
gdf = gpd.read_file(shapefile_path)

# Read the raster file
with rasterio.open(raster_path) as src:
    raster_data = src.read(1)  # Assuming it's a single-band raster
    transform = src.transform


# Function to calculate percentage overlap
def calculate_overlap_percentage(geometry, raster_data, transform):
    if geometry.is_empty:
        return 0.0
    # Wrap the single geometry in a list to make it iterable
    shapes = [geometry]
    mask = geometry_mask(shapes, out_shape=raster_data.shape, transform=transform, invert=True)
    return np.sum(mask) / mask.size


# Add a new column with the percentage of overlap
gdf['overlap_percentage'] = gdf['geometry'].apply(
    lambda geom: calculate_overlap_percentage(geom, raster_data, transform))

# Print the GeoDataFrame with the new column
print(gdf[['vatnLnr', 'overlap_percentage']])

# Save the GeoDataFrame back to a shapefile if needed
# gdf.to_file(r"path_to_save\output_shapefile.shp")
