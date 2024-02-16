import rasterio
from rasterio.merge import merge
from rasterio.plot import show

# List of DEM tiles paths
dem_files = [
    "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6900_2_10m_z33.tif",
    "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6800_1_10m_z33.tif",
    "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6801_4_10m_z33.tif",
    "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/metadata/dtm10_6901_3_10m_z33.tif"
]

# Open each DEM tile
src_files_to_mosaic = []
for file in dem_files:
    src = rasterio.open(file)
    src_files_to_mosaic.append(src)

# Merge DEM tiles
mosaic, out_trans = merge(src_files_to_mosaic)

# Save the merged DEM
out_meta = src.meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans})

output_file = "/media/snowman/LaCie/cascading_slushflow/fonnbu/dtm10/merged_dem.tif"
with rasterio.open(output_file, "w", **out_meta) as dest:
    dest.write(mosaic)

print("Merged DEM saved to:", output_file)
