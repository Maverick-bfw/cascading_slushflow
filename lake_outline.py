import rasterio
import numpy as np
from skimage.morphology import binary_dilation, erosion, label

lake_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/trimmed_lakes_raster.tif"
output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/rings.tif"

with rasterio.open(lake_file) as lake_src:
    lake = lake_src.read(1)  # Read lake raster data
    profile = lake_src.profile  # Get profile from the lake raster for output raster

    # Define a threshold value to binarize the lake raster
    threshold = 0  # Adjust as needed based on your specific raster values

    # Binarize the lake raster using the threshold
    binary_lake = lake > threshold

    # Label connected regions (clusters) in the binary lake raster
    labeled_lake = label(binary_lake, connectivity=2)  # Set connectivity to 2 for diagonal connections

    # Initialize the output data array with zeros
    output_data = np.zeros_like(lake)

    # Iterate over unique labels (clusters)
    for cluster_label in np.unique(labeled_lake):
        if cluster_label == 0:  # Skip background label (0)
            continue
        if cluster_label > 60:
            continue

        print(cluster_label)
        # Create a binary mask for the current cluster
        cluster_mask = labeled_lake == cluster_label

        # Erode the cluster mask to include diagonal cells
        eroded_mask = erosion(cluster_mask, np.ones((3, 3)))

        # Find the difference between the eroded mask and the original mask
        outline = cluster_mask ^ eroded_mask

        # Assign the cluster label to the cells in the outline
        output_data[outline] = cluster_label

        # Perform dilation to get the surrounding ring
        ring = binary_dilation(cluster_mask) & ~cluster_mask

        # Assign the cluster label to the cells in the ring
        output_data[ring] = cluster_label


with rasterio.open(output_file, "w", **profile) as dst:
    dst.write(output_data, 1)
