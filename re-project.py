import gdal
from pathlib import Path
def clip_raster(input_raster_path, output_raster_path, extent):
    # Open the input raster
    input_raster = gdal.Open(input_raster_path, gdal.GA_ReadOnly)
    if input_raster is None:
        print("Failed to open the input raster.")
        return

    # Get the projection and geotransform
    projection = input_raster.GetProjection()
    geotransform = input_raster.GetGeoTransform()

    # Get raster dimensions
    cols = input_raster.RasterXSize
    rows = input_raster.RasterYSize

    # Create a new raster for the clipped area
    output_raster = gdal.GetDriverByName('GTiff').Create(output_raster_path, cols, rows, 1, gdal.GDT_Float32)
    output_raster.SetProjection(projection)
    output_raster.SetGeoTransform(geotransform)

    # Set the extent for the clipping
    output_raster.SetGeoTransform(extent)

    # Perform the clip
    gdal.ReprojectImage(input_raster, output_raster, None, None, gdal.GRA_NearestNeighbour)

    # Close the datasets
    input_raster = None
    output_raster = None

# Path to the DEM raster

#file_path = Path("/home/chris/OneDrive/cascading_slushflow/") # linux path
file_path = Path("C:/Users/cda055/OneDrive - UiT Office 365/cascading_slushflow/") # windows path
dem_raster_path = file_path / "dtm10_6901_3_10m_z33.tif"

# Path to the "flow-py.tif" raster
flow_raster_path = file_path / "flow-py-norway_travel_angle_18.tif"
output_clip_path = file_path / "output_clipped_raster.tif"

# Open the DEM raster to get its extent
dem_raster = gdal.Open(dem_raster_path, gdal.GA_ReadOnly)
if dem_raster is None:
    print("Failed to open the DEM raster.")
    exit(1)

# Get the extent of the DEM raster
extent = dem_raster.GetGeoTransform()
# Adjust the extent as needed based on the specific area you want to clip



# Clip the "flow-py.tif" raster to the extent of the DEM raster
clip_raster(flow_raster_path, output_clip_path, extent)

print("Clipping completed. Clipped raster saved at:", output_clip_path)
