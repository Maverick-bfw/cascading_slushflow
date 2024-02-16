
import rasterio
from osgeo import gdal
# File path to the raster file
#raster_file_path = '/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster.tif'
#raster_file_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/merged_dem.tif"
raster_file_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/trimmed_lakes_raster.tif"

try:
    with rasterio.open(raster_file_path) as rio_dataset:
        print("Raster file ", raster_file_path)
        print("\nRasterio Info:")
        print("Driver: {}".format(rio_dataset.driver))
        print("Bounds: {}".format(rio_dataset.bounds))
        print("Width, Height: {}, {}".format(rio_dataset.width, rio_dataset.height))
        print("Number of Bands: {}".format(rio_dataset.count))
        print("Coordinate Reference System (CRS): {}".format(rio_dataset.crs))
except Exception as e:
    print("Error opening the raster file with Rasterio:", str(e))

"""
# Using GDAL to open and read information
gdal_dataset = gdal.Open(raster_file_path)

if gdal_dataset is not None:
    print("Raster file " , raster_file_path)
    print("GDAL Info:")
    print("Driver: {}/{}".format(gdal_dataset.GetDriver().ShortName, gdal_dataset.GetDriver().LongName))
    print("Size: {} x {}".format(gdal_dataset.RasterXSize, gdal_dataset.RasterYSize))
    print("Number of Bands: {}".format(gdal_dataset.RasterCount))
    print("Projection: {}".format(gdal_dataset.GetProjection()))
    print("GeoTransform: {}".format(gdal_dataset.GetGeoTransform()))

    # Get the raster band
    band = gdal_dataset.GetRasterBand(1)

    # Get the data type of the band
    data_type = gdal.GetDataTypeName(band.DataType)

    print("Data type of the raster band:", data_type)
    # Close the GDAL dataset
    gdal_dataset = None
else:
    print("Error opening the raster file with GDAL")
"""
# Using Rasterio to open and read information

raster_file_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/trimmed_DEM_raster.tif"
try:
    with rasterio.open(raster_file_path) as rio_dataset:
        print("Raster file ", raster_file_path)
        print("\nRasterio Info:")
        print("Driver: {}".format(rio_dataset.driver))
        print("Bounds: {}".format(rio_dataset.bounds))
        print("Width, Height: {}, {}".format(rio_dataset.width, rio_dataset.height))
        print("Number of Bands: {}".format(rio_dataset.count))
        print("Coordinate Reference System (CRS): {}".format(rio_dataset.crs))
except Exception as e:
    print("Error opening the raster file with Rasterio:", str(e))

