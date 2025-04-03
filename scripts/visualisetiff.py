import rasterio     #higher level package raster functions
from rasterio.merge import merge
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

#eventually change this is own tiff class

class HandleTiff:
    ''' Class to handle geotiff files'''

########################################

    #def __init__(self,filename):
    #  '''Class initialiser
    #  Does nothing as this is only an example'''
#
    #sort

########################################

    def merge_tiles(self, input_dir, output_path):

        # call all tif files in input folder
        tile_files = glob.glob(os.path.join(input_dir,'*tif'))

        # open tiles
        src_files_to_mosaic = []    # create empty array
        for fp in tile_files:       # loop over file paths
            src = rasterio.open(fp)
            src_files_to_mosaic.append(src)

        # merge with rasterio + maintain georeference
        mosaic, out_trans = merge(src_files_to_mosaic)

        # set mo data to NaN before export
        mosaic = np.where(mosaic == -999.0, np.nan, mosaic)

        # save merged file
        with rasterio.open(output_path, "w", driver='GTiff', #create output_tiff, specify format
                           height=mosaic.shape[1],  # tiff is same height as input
                           width=mosaic.shape[2],   # tiff is same width as input
                           count=1, dtype=rasterio.float32,     # can handle NaN
                           crs=src_files_to_mosaic[0].crs,  # uses same crs as input file
                           transform=out_trans) as dest:
                            dest.write(mosaic[0], 1)    # writes to first band 

        for src in src_files_to_mosaic:     # closes to free space 
                src.close()

        print(f'Merged DEM is saved as {output_path}')

    def visualise_tiff(self, tiff_path,plot_filename):
        # open the tiff to visualise with rasterio
        dataset = rasterio.open(tiff_path)
        # print raster dimensions
        print(f'The raster is {dataset.width} x {dataset.height}  pixels')
        print(dataset.crs)      #print projection

        merged_image = dataset.read(1)  #read band

        # make plot
        plt.figure(figsize=(6,10))
        plt.imshow(merged_image, cmap='cividis')
        plt.colorbar(label='Elevation (m)')      # legend
        plt.xlabel('Metres', fontsize=14)
        plt.ylabel('Metres', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        plt.show()