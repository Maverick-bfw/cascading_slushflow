from osgeo import gdal, ogr, osr
from pathlib import Path

# Paths to the input files
#file_path = Path("/home/chris/OneDrive/cascading_slushflow/") # linux path
file_path = Path("C:/Users/cda055/OneDrive - UiT Office 365/cascading_slushflow/") # windows path
lakes_shapefile_path = file_path / Path("lakes/NVEData/Innsjo/Innsjo_Innsjo.shp")
avalanche_raster_path = file_path / Path("Flow-py_18deg_avalanche/flow-py-norway_travel_angle_18.tif")
output_raster_path = file_path / "output_rasterized_lakes.tif"

# Open the avalanche raster to get its properties
gdal.SetConfigOption('GTIFF_SRS_SOURCE', 'EPSG')

avalanche_ds = gdal.Open(str(avalanche_raster_path))
avalanche_band = avalanche_ds.GetRasterBand(1)
avalanche_gt = avalanche_ds.GetGeoTransform()
projection = avalanche_ds.GetProjection()

# Get the extent and resolution from the avalanche raster
xmin, ymax, xmax, ymin = avalanche_gt[0], avalanche_gt[3], avalanche_gt[0] + avalanche_ds.RasterXSize * avalanche_gt[1], avalanche_gt[3] - avalanche_ds.RasterYSize * avalanche_gt[5]
pixel_size_x = avalanche_gt[1]
pixel_size_y = avalanche_gt[5]
x_res = avalanche_ds.RasterXSize
y_res = avalanche_ds.RasterYSize

# Create a blank raster to burn the lakes into
target_ds = gdal.GetDriverByName('GTiff').Create(str(output_raster_path), x_res, y_res, 1, gdal.GDT_Byte)
target_ds.SetGeoTransform((xmin, pixel_size_x, 0, ymax, 0, pixel_size_y))
target_ds.SetProjection(projection)
band = target_ds.GetRasterBand(1)
band.SetNoDataValue(0)

# Open the lakes shapefile
lakes_ds = ogr.Open(str(lakes_shapefile_path))
lakes_layer = lakes_ds.GetLayer()

# Rasterize the lakes onto the blank raster
gdal.RasterizeLayer(target_ds, [1], lakes_layer, burn_values=[1])

# Close the datasets
target_ds = None
lakes_ds = None
avalanche_ds = None
