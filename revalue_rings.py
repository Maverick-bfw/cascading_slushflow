import rasterio

# Define paths to the output raster and DEM raster
rings_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/rings.tif"
dem_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/trimmed_DEM_raster.tif"
output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/rings_DEM.tif"

# Open the output raster and DEM raster
with rasterio.open(rings_file) as output_src, rasterio.open(dem_file) as dem_src:
    # Read the data and transformation matrix for the output raster and DEM raster
    output_data = output_src.read(1)
    output_transform = output_src.transform
    dem_data = dem_src.read(1)
    dem_transform = dem_src.transform

    # Find cells with values greater than 0 in the output raster
    cells_greater_than_zero = output_data > 0

    # Loop over each cell with value greater than 0
    for row, col in zip(*cells_greater_than_zero.nonzero()):
        # Get the coordinates of the cell in the output raster
        output_coords = output_transform * (col, row)

        # Convert output raster coordinates to DEM raster coordinates
        dem_col, dem_row = ~dem_transform * output_coords

        # Round DEM coordinates to integer indices
        dem_col, dem_row = int(round(dem_col)), int(round(dem_row))

        # Update the value of the cell in the output raster with the corresponding elevation value from the DEM
        output_data[row, col] = dem_data[dem_row, dem_col]

# Save the modified output raster
with rasterio.open(output_file, 'w', driver='GTiff',
                   width=output_data.shape[1], height=output_data.shape[0],
                   count=1, dtype=output_data.dtype,
                   crs=output_src.crs, transform=output_transform) as dst:
    dst.write(output_data, 1)
