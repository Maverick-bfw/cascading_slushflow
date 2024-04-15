import rasterio
import numpy as np
from skimage.morphology import binary_dilation, erosion, label
from revalue_rings import revalue_cells
lake_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/trimmed_lakes_raster.tif"
output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/drainage.tif"
dem_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/trimmed_DEM_raster.tif"

with rasterio.open(lake_file) as lake_src, rasterio.open(dem_file) as dem_src: # open lakes and dem files
    lake = lake_src.read(1)  # Read lake raster data
    lake_transform = lake_src.transform
    dem_data = dem_src.read(1)
    dem_transform = dem_src.transform

    profile = lake_src.profile  # Get profile from the lake raster for output raster

    # Define a threshold value to binarize the lake raster
    threshold = 0  # Adjust as needed based on your specific raster values

    # Binarize the lake raster using the threshold
    binary_lake = lake > threshold
    reversed_binary = np.invert(binary_lake)
    # Label connected regions (clusters) in the binary lake raster
    labeled_lake = label(binary_lake, connectivity=2)  # Set connectivity to 2 for diagonal connections
    mask = erosion(reversed_binary, np.ones((3,3)))
   #binary_extended_lakes = labeled_lake > threshold
    rings = np.invert(binary_lake ^ mask)
    # Initialize the output data array with zeros
    output_data = np.zeros_like(lake)
    """
    # Iterate over unique labels (clusters)
    for cluster_label in np.unique(labeled_lake):
        if cluster_label == 0:  # Skip background label (0)
            continue
        if cluster_label > 10:
            continue
        print(cluster_label)
    """

    # Create a binary mask for the current cluster
    cluster_mask = labeled_lake != lake #cluster_label

    # Erode the cluster mask to include diagonal cells
    eroded_mask = erosion(cluster_mask, np.ones((3, 3)))

    # Find the difference between the eroded mask and the original mask
    outline = cluster_mask ^ eroded_mask

    # Assign the cluster label to the cells in the outline
    #output_data[outline] = cluster_label

    # Perform dilation to get the surrounding ring
    #ring = binary_dilation(cluster_mask) & ~cluster_mask
    # this is where to revalue rings based on DEM
    ring = revalue_cells(outline, lake_transform, dem_transform, dem_data)
    # this is where to find lowest values
    # Assign the cluster label to the cells in the ring
    output_data = np.where(ring > 0, ring, output_data)


with rasterio.open(output_file, "w", **profile) as dst:
    dst.write(output_data, 1)
