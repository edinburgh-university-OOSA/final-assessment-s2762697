import rasterio     #higher level package raster functions
import matplotlib.pyplot as plt
import numpy as np


dataset = rasterio.open('../Data/lvisDEM_PIG6.tif')
# print raster dimensions
print(f'The raster is {dataset.width} x {dataset.height}  pixels')
print(dataset.crs)      #print projection

lvis_image = dataset.read(1)  #read band

# set no values to not a number
lvis_image = np.where(lvis_image ==-999.0, np.nan, lvis_image)
plt.imshow(lvis_image, cmap='cividis')
plt.colorbar(label='Elevation (m)')      # legend
plt.xlabel('metres') # check this
plt.ylabel('metres')  # check this
plt.show()
#print(np.unique(lvis_image))