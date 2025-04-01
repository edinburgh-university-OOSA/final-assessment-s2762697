import rasterio     #higher level package raster functions
from rasterio.merge import merge
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

#eventually change this so that visualise tiff is also in plot class???

# input and output directories
tiles_dir2009 = '../Data'
output_folder = '../Outputs'
output_tiff = os.path.join(output_folder, '2009_DEM')

# check folder exists and create if not
os.makedirs(output_folder, exist_ok=True)


# call all tif files in input folder
tile_files = glob.glob(os.path.join(tiles_dir2009,'*tif'))

# open tiles
src_files_to_mosaic = []    # create empty array
for fp in tile_files:       # loop over file paths
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)

# merge with rasterio + georeference
mosaic, out_trans = merge(src_files_to_mosaic)

# set mo data to NaN before export
mosaic = np.where(mosaic == -999.0, np.nan, mosaic)

# save merged file
with rasterio.open(output_tiff, "w", driver='GTiff', #create output_tiff, specify format
                   height=mosaic.shape[1],  # tiff is same height as input
                   width=mosaic.shape[2],   # tiff is same width as input
                   count=1, dtype=rasterio.float32,
                   crs=src_files_to_mosaic[0].crs,
                   transform=out_trans) as dest:
                    dest.write(mosaic[0], 1)

for src in src_files_to_mosaic:
        src.close()

#print(f'Merged DEM is saved as {output_tiff}')

dataset = rasterio.open('../Outputs/2009_DEM')
# print raster dimensions
print(f'The raster is {dataset.width} x {dataset.height}  pixels')
print(dataset.crs)      #print projection

merged_image = dataset.read(1)  #read band

# make plot
plt.imshow(merged_image, cmap='cividis')
plt.colorbar(label='Elevation (m)')      # legend
plt.xlabel('metres') # check this
plt.ylabel('metres')  # check this
plt.show()
#print(np.unique(lvis_image))