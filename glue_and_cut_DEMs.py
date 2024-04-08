"""
### saving file as .tif file
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
from rasterio.features import geometry_mask
from rasterio.warp import transform_bounds

# Load the merged DEM to get its bounding box
merged_dem_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster.tif"
with rasterio.open(merged_dem_path) as src_dem:
    dem_bounds = src_dem.bounds

# Load the lakes raster
lakes_raster_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/merged_dem.tif"
with rasterio.open(lakes_raster_path) as src_lakes:
    # Get the bounds of the lakes raster
    lakes_bounds = src_lakes.bounds

    # Intersect the bounds of the lakes raster with the bounds of the DEM
    intersected_bounds = (
        max(dem_bounds.left, lakes_bounds.left),
        max(dem_bounds.bottom, lakes_bounds.bottom),
        min(dem_bounds.right, lakes_bounds.right),
        min(dem_bounds.top, lakes_bounds.top)
    )

    # Create a geometry based on the intersected bounds
    intersected_geom = box(*intersected_bounds)

    # Mask the lakes raster using the intersected geometry
    out_image, out_transform = mask(src_lakes, [intersected_geom], crop=True)

    # Update the metadata for the output raster
    out_meta = src_lakes.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform,
                     "bounds": intersected_bounds})

    # Write the masked lakes raster to a new file
    output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/trimmed_DEM_raster.asc"
    with rasterio.open(output_file, "w", **out_meta) as dest:
        dest.write(out_image)

print("Trimmed lakes raster saved to:", output_file)
"""


### saving as .asc file
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import numpy as np

# Load the merged DEM to get its bounding box
merged_dem_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/zoom/rel1.tif"
with rasterio.open(merged_dem_path) as src_dem:
    dem_bounds = src_dem.bounds

# Load the lakes raster
lakes_raster_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/zoom/dem1.tif"
with rasterio.open(lakes_raster_path) as src_lakes:
    # Get the bounds of the lakes raster
    lakes_bounds = src_lakes.bounds

    # Intersect the bounds of the lakes raster with the bounds of the DEM
    intersected_bounds = (
        max(dem_bounds.left, lakes_bounds.left),
        max(dem_bounds.bottom, lakes_bounds.bottom),
        min(dem_bounds.right, lakes_bounds.right),
        min(dem_bounds.top, lakes_bounds.top)
    )

    # Create a geometry based on the intersected bounds
    intersected_geom = box(*intersected_bounds)

    # Mask the lakes raster using the intersected geometry
    out_image, out_transform = mask(src_lakes, [intersected_geom], crop=True)

# Convert the masked raster data to ASCII format
output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/zoom/dem1.asc"
with open(output_file, 'w') as f:
    f.write("NCOLS {}\n".format(out_image.shape[2]))
    f.write("NROWS {}\n".format(out_image.shape[1]))
    f.write("XLLCORNER {}\n".format(intersected_bounds[0]))
    f.write("YLLCORNER {}\n".format(intersected_bounds[1]))
    f.write("CELLSIZE {}\n".format(out_transform[0]))
    f.write("NODATA_VALUE {}\n".format(src_lakes.nodata))

    # Iterate over each row and column of the masked array
    for row in range(out_image.shape[1]):
        for col in range(out_image.shape[2]):
            # Check if the pixel value is nodata
            if np.isnan(out_image[0, row, col]):
                f.write("{} ".format(int(src_lakes.nodata)))
            else:
                f.write("{} ".format(int(out_image[0, row, col])))
        f.write("\n")

print("Trimmed lakes raster saved to:", output_file)
