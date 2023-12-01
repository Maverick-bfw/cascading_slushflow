from osgeo import gdal
import numpy as np
from skimage import filters
from scipy import ndimage

# Load the DEM using GDAL
file_path = "/home/chris/OneDrive/cascading_slushflow/"
dem_file_path = file_path + "dtm10_6801_4_10m_z33.tif"

output_mask_path = file_path + "lakes.tif"

dem_dataset = gdal.Open(dem_file_path)
dem_array = dem_dataset.ReadAsArray()

# Compute the gradient/slope of the DEM
gradient = filters.sobel(dem_array)

# Threshold the gradient to identify flat areas (potential water bodies)
gradient_threshold =0.5  # Adjust based on your DEM and requirements
flat_areas = gradient < gradient_threshold

# Use morphological operations to further refine the mask
structuring_element = np.ones((3, 3), dtype=bool)
flat_areas = ndimage.binary_erosion(flat_areas, structure=structuring_element, iterations=2)

# Create a new GeoTIFF for the water bodies mask
driver = gdal.GetDriverByName('GTiff')
rows, cols = flat_areas.shape
new_dataset = driver.Create(output_mask_path, cols, rows, 1, gdal.GDT_Byte)
new_dataset.SetGeoTransform(dem_dataset.GetGeoTransform())
new_dataset.SetProjection(dem_dataset.GetProjection())
new_dataset.GetRasterBand(1).WriteArray(flat_areas.astype(np.uint8))

# Close datasets
new_dataset = None
dem_dataset = None

print("Water bodies mask saved successfully at:", output_mask_path)