import rasterio
import numpy as np
from skimage.morphology import binary_dilation
from skimage.measure import label

lake_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster.tif"
output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/rings.tif"



with rasterio.open(lake_file) as lake_src:
    lake = lake_src.read(1)  # Read lake raster data
    profile = lake_src.profile  # Get profile from the lake raster for output raster

    # Define a threshold value to binarize the lake raster
    threshold = 0  # Adjust as needed based on your specific raster values

    # Binarize the lake raster using the threshold
    binary_lake = lake > threshold

    # Label connected regions (clusters) in the binary lake raster
    labeled_lake = label(binary_lake)

    # Initialize the output data array with zeros
    output_data = np.zeros_like(lake)

    # Iterate over unique labels (clusters)
    for cluster_label in np.unique(labeled_lake):
        if cluster_label == 0:  # Skip background label (0)
            continue

        # Create a binary mask for the current cluster
        cluster_mask = labeled_lake == cluster_label

        # Perform dilation to get the surrounding ring
        ring = binary_dilation(cluster_mask) & ~cluster_mask

        # Assign the cluster label to the cells in the ring
        output_data[ring] = cluster_label


with rasterio.open(output_file, "w", **profile) as dst:
    dst.write(output_data, 1)
