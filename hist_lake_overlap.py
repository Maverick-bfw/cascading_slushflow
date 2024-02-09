import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show_hist
import numpy as np
# Paths to the raster files
lakes_raster_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster.tif"
output_combined_path = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_combined.tif"

# Function to read raster values and flatten the array
def read_raster_values(raster_path):
    with rasterio.open(raster_path) as src:
        array = src.read(1)  # Read the first band
        max_lakes_count = array.max()
        print("max lakes no ", max_lakes_count)
        return array

# Read raster values
lakes_values = read_raster_values(lakes_raster_path)
output_combined_values = read_raster_values(output_combined_path)

# Set bins as integers up to the maximum value in the lakes raster, excluding 0

bins = range(1, np.max(lakes_values) + 1)
# Plotting histograms
plt.hist(lakes_values.flatten(), bins=bins, alpha=0.5, label='Lakes Raster', color='blue')
plt.hist(output_combined_values.flatten(), bins=bins, alpha=0.5, label='Output Combined Raster', color='orange')

plt.xlabel('Raster Cell Values')
plt.ylabel('Frequency')
plt.title('Histogram of Lakes Raster and Output Combined Raster')
plt.legend()
plt.show()
