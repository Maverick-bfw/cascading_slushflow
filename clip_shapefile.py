import geopandas as gpd
import rasterio
from rasterio import features
from shapely.geometry import box
from fiona.crs import from_epsg

# Define paths to your files
shapefile_path = r'D:\cascading_slushflow\National_data\lakes\NVEData\Innsjo\Innsjo_Innsjo.shp'
rasterfile_path = r'D:\cascading_slushflow\fonnbu\fonnbu_avalanche.tif'
output_shapefile_path = r'D:\cascading_slushflow\fonnbu\Fonnbu_lakes.shp'

# Read the shapefile and raster
gdf = gpd.read_file(shapefile_path)
with rasterio.open(rasterfile_path) as src:
    raster_extent = box(*src.bounds)

# Clip the shapefile to the raster extent
clipped_gdf = gdf.cx[raster_extent.bounds[0]:raster_extent.bounds[2],
                    raster_extent.bounds[1]:raster_extent.bounds[3]]

# Create a GeoDataFrame from the clipped geometry
clipped_gdf = gpd.GeoDataFrame(geometry=[raster_extent.intersection(geom) for geom in clipped_gdf.geometry],
                               crs=gdf.crs)

# Save the clipped shapefile
clipped_gdf.to_file(output_shapefile_path)

print(f"Clipped shapefile saved to {output_shapefile_path}")
