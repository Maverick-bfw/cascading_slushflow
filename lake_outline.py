import rasterio
import numpy as np
from skimage.morphology import binary_dilation, erosion, label
from rasterio.warp import transform_geom
from rasterio.transform import from_origin

lake_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/output_lakes_raster.tif"
output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/start_zones.tif"



with rasterio.open(lake_file) as lake_src:
    lake = lake_src.read(1)  # Read lake raster data
    lake_profile = lake_src.profile  # Get profile from the lake raster for output raster
    lake_transform = lake_src.transform  # Get the transformation matrix

    # Define a threshold value to binarize the lake raster
    threshold = 0  # Adjust as needed based on your specific raster values

    # Binarize the lake raster using the threshold
    binary_lake = lake > threshold

    # Label connected regions (clusters) in the binary lake raster
    labeled_lake = label(binary_lake, connectivity=2)  # Set connectivity to 2 for diagonal connections

    # Initialize the output data array with zeros
    output_data = np.zeros_like(lake)

    # Open all DEM files
    dem_files = [
        rasterio.open(dem_file_path) for dem_file_path in [
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6800_1_10m_z33.tif",
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6801_4_10m_z33.tif",
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6900_2_10m_z33.tif",
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6901_3_10m_z33.tif"
        ]
    ]

    # Iterate over unique labels (clusters)
    for cluster_label in np.unique(labeled_lake):
        if cluster_label == 0:  # Skip background label (0)
            continue
        if cluster_label > 40:
            continue
        if cluster_label != 9:
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

        # Define the bounds of the ring
        ring_bounds = [
            min(col for col, row in zip(*ring.nonzero())),
            min(row for col, row in zip(*ring.nonzero())),
            max(col for col, row in zip(*ring.nonzero())),
            max(row for col, row in zip(*ring.nonzero()))
        ]

        # Determine the DEM tiles covering the lake cluster
        dem_files = [
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6800_1_10m_z33.tif",
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6801_4_10m_z33.tif",
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6900_2_10m_z33.tif",
            "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6901_3_10m_z33.tif"
        ]

        # Read elevation values from DEM files and assign to the cells in the ring
        for dem_file in dem_files:
            with rasterio.open(dem_file) as dem_src:
                dem_data = dem_src.read(1)  # Read DEM data
                dem_transform = dem_src.transform  # Get the transformation matrix

                # Convert ring bounds to pixel coordinates in the DEM
                ring_bounds_px = rasterio.transform.rowcol(dem_transform, *lake_transform * ring_bounds[::2]) + \
                                 rasterio.transform.rowcol(dem_transform, *lake_transform * ring_bounds[1::2])
                ring_bounds_px = [int(np.round(coord)) for coord in ring_bounds_px]

                # Ensure ring bounds are within the DEM data extent

                ring_bounds_px = [min(ring_bounds_px[0], dem_data.shape[1] - 1),
                                  min(ring_bounds_px[1], dem_data.shape[0] - 1),
                                  max(ring_bounds_px[2], 0),
                                  max(ring_bounds_px[3], 0)]

                # Extract the portion of the ring within the DEM tile
                ring_data = dem_data[ring_bounds_px[1]:ring_bounds_px[3] + 1, ring_bounds_px[0]:ring_bounds_px[2] + 1]

                # Update output data with ring data
                output_data[ring_bounds_px[1]:ring_bounds_px[3] + 1, ring_bounds_px[0]:ring_bounds_px[2] + 1] = ring_data

with rasterio.open(output_file, "w", **lake_profile) as dst:
    dst.write(output_data, 1)