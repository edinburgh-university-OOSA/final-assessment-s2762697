
'''An example of how to use the LVIS python scripts'''

# import libraries
from pyproj import Transformer
from matplotlib import pyplot as plt
from glob import glob
import tracemalloc
import argparse
#import psutil

#import other classes and functions
from processLVIS import lvisGround
from tiffExample import writeTiff

##########################################



class plotLVIS(lvisGround):
  '''A class, ineriting from lvisground (from processLVIS) and a plotting method'''
  
  def reprojectLVIS(self,outEPSG):
    '''Reproject the data'''
    #set projections as direct strings
    inEPSG = "EPSG:4326"
    outEPSG = f"EPSG: {outEPSG}"
    #use transformer so dont deprecate with transform
    transformer = Transformer.from_crs(inEPSG, outEPSG, always_xy=True) #always long,lat order
    #reproject
    self.x, self.y = transformer.transform(self.lon, self.lat)


  def plotSingleWave(self, index, save_path='Waveform.png'):
    '''Plot single waveform if it exiss and exports as a png'''
    try:    #try-except so that it doesnt crash if index with no data is selected
      elevation, waveform = self.getOneWave(index) #waveform  at index 20  #update
      plt.xlabel("Waveform return")
      plt.ylabel("Elevation (m)")
      plt.plot(waveform, elevation, c='purple') 
      plt.savefig(save_path, bbox_inches='tight')
      print(f'Waveform has been saved to {save_path}')
      plt.show()
    except IndexError as e: #raise error if no data
      print(e)


  def makeDEM(self, res, tiffName):
    '''convert data to a goetiff (from tiffExample.py)'''
    #change filename
    writeTiff(data=self.zG, x=self.x, y=self.y, res=res, filename=tiffName, epsg=3031)
    return 

##########################################

if __name__=="__main__":
  '''Main block'''

  #start tracking RAM
  tracemalloc.start()

  filename='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_058456.h5'   

  b=plotLVIS(filename,onlyBounds=True)    #first index in list

#   loop for subdivisions 
  subset_size = 3 #check what this means 
  x_step = (b.bounds[2]-b.bounds[0])/subset_size  #x length/20 #update
  y_step = (b.bounds[3]-b.bounds[1])/subset_size  #y length/20

  for i in range(subset_size):    #loop for x axis
    for j in range(subset_size):    #loop for y axis
      x0=b.bounds[0] + i * x_step   #fist x
      y0=b.bounds[1] + j * y_step   #first y
      x1 = x0 + x_step    #end x
      y1 = y0 + y_step    #end y  
      #check bounds
      print(f'Subset bounds{x0, y0} to {x1, y1}')


      lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)

      # check that it contains some data
      if(lvis.nWaves==0):
        continue

      # Make DEM as a geotiff
      lvis.reprojectLVIS(3031)  # call reproject function -move to process
      lvis.estimateGround()     # call find ground function
      tiffName = "Data/lvisDEM_PIGloop.x"+str(x0)+".y."+str(y0)+".tif"   #filename with bands
      lvis.makeDEM(30, tiffName)       #resolution 


  print(f'Each geotiff is split into {subset_size} x {subset_size} tiles') 

  
  current, peak = tracemalloc.get_traced_memory() #both needed as returns a tuple
  peak_GB = peak/(1024**3)
  print(f'Peak memory used was: {peak_GB:.2f} GB')
  print(current,peak)
