import rasterio     #higher level package raster functions
import matplotlib.pyplot as plt

dataset = rasterio.open('lvisDEMloop.x277.45731593434334.y.-68.80784508465653.tif')


print(dataset.width)    #print width of raster
print(dataset.height)   #print height of raster
print(dataset.crs)      #print projection

lvis_image = dataset.read(1)
#lvis_image == [-999.0 = nan]
plt.imshow(lvis_image)
plt.colorbar()      #legend
#plt.xlabel('Longitude')
#plt.ylabel('Latitude')
plt.show()

#is this visualising on elevation 


#new_dataset = rasterio.open(outName,'w', driver = 'GTiff', height = dataset8.height,
#                            width = dataset8.width, count = 1, dtype = NDVI_image.dtype,
#                            crs = dataset8.crs, ransform = dataset8.transform)
#new_dataset.write(NDVI_image, 1)
#new_dataset.nodata = -999.0
#new_dataset.close()
