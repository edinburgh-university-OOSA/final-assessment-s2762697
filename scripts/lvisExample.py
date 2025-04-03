'''An example of how to use the LVIS python scripts'''

# import libraries
from pyproj import Transformer
from matplotlib import pyplot as plt
from glob import glob
import tracemalloc
import argparse
import os

#import other classes and functions
from processLVIS import lvisGround
from tiffExample import writeTiff
from visualisetiff import HandleTiff

##########################################

def chooseArg():
  '''Method to pick arguements from command line'''
  # create argparse object
  parser = argparse.ArgumentParser(description='Choose a single waveform from LVIS data')
  # waveform index
  parser.add_argument('-i', type=int, default=155892, help = 'Index of waveform')
  # waveform file name 
  parser.add_argument('-o', type=str, default='Waveform.png',
                      help='Output file name of waveform')
  # merged DEM tiff name
  parser.add_argument('--tiff_output', type=str, default='2009_DEM.tif', help='Name of the output TIFF file')
  # resolution with threshold
  parser.add_argument('--res', type=int, default=30, help='Resolution for DEM creation (between 20 and 100)')


  # parse the command line into an object
  args = parser.parse_args()

  # check threshold for resolution 
  if not(20<= args.res <= 100):
    print("Warning, resolution must be between 20 and 100. Using default (30)")
    args.res = 30 

  return args

class plotLVIS(lvisGround):
  '''A class, ineriting from lvisground (from processLVIS) and a plotting method'''

  def plotSingleWave(self, index, save_path='Outputs/Waveform.png'):
    '''Plot single waveform if it exiss and exports as a png'''
    try:    #try-except so that it doesnt crash if index with no data is selected
      elevation, waveform = self.getOneWave(index) #waveform  at chosen index (default=xx) - update
      plt.xlabel("Waveform return")
      plt.ylabel("Elevation (m)")
      plt.plot(waveform, elevation, c='purple') 
      plt.savefig(save_path, bbox_inches='tight')
      print(f'Waveform has been saved to {save_path}')
      plt.show()
    except IndexError as e: #raise error if no data
      print(e)

  def makeDEM(self, resolution, tiffName):
    '''convert data to a goetiff (from tiffExample.py)'''
    # call function from tiffExample.py
    writeTiff(data=self.zG, x=self.x, y=self.y, res=resolution, filename=tiffName, epsg=3031)
    return 

##########################################

if __name__=="__main__":
  '''Main block'''

  # start tracking RAM
  tracemalloc.start()

  command = chooseArg()

##########################################
  #for looping through all files
  #filelist_2009 = glob('/geos/netdata/oosa/assignment/lvis/2009/*.h5')  #only.h5 files
  #print(filelist_2009)
  #filelist_2015 = glob('/geos/netdata/oosa/assignment/lvis/2015/*.h5')  #only.h5 files
  #print(filelist_2015)

  # file over Pine Island Glacier used in Task 1 and Task 2
  filename='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_058456.h5'  #single file test

##############################################
  # find bounds
  b=plotLVIS(filename,onlyBounds=True)    #first index in list
  
  # loop for tile subdivisions 
  subset_size = 3 #check what this means 
  x_step = (b.bounds[2]-b.bounds[0])/subset_size  #x length/20 #update
  y_step = (b.bounds[3]-b.bounds[1])/subset_size  #y length/20

  tile_number = 1   # first tile is 1

  for i in range(subset_size):    #loop for x axis
    for j in range(subset_size):    #loop for y axis
      x0=b.bounds[0] + i * x_step   #fist x
      y0=b.bounds[1] + j * y_step   #first y
      x1 = x0 + x_step    #end x
      y1 = y0 + y_step    #end y  
      # check bounds
      print(f'Tile {tile_number} has subset bounds {x0:.3f},{y0:.3f} to {x1:.3f},{y1:.3f}')
      
      # all inside loop
      # read in all data within our spatial subset
      lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1, setElev=True)   #read in elev

      # check that it contains some data
      if(lvis.nWaves==0):
        tile_number +=1   #if no data still need to add
        continue

      # Make DEM as a geotiff
      lvis.reprojectLVIS(3031)  # call reproject function -move to process
      lvis.estimateGround()     # call find ground function
      tiffName = f"../Data/lvisDEM_PIG{tile_number}.tif"   #filename with tile identifier
      lvis.makeDEM(command.res, tiffName)       #resolution 

      # tile counter at end of loop
      tile_number +=1   #after it is called

  # Outside loop
  # call function to plot single waveform
 #lvis.plotSingleWave(index=command.index)
print(f'Each geotiff is split into {subset_size} x {subset_size} tiles') 
  
# specify places
tiles_dir2009 = '../Data'   # specify input dir
output_folder = '../Outputs'    # specify output dir
os.makedirs(output_folder, exist_ok=True) # check folder exists and create if not
output_tiff = os.path.join(output_folder, command.tiff_output)

# call functions
get_tiff = HandleTiff()
get_tiff.merge_tiles(tiles_dir2009, output_tiff)
get_tiff.visualise_tiff(output_tiff)

# Memory tracking
current, peak = tracemalloc.get_traced_memory() #both needed as returns a tuple
peak_GB = peak/(1024**3)
print(f'Peak memory used was: {peak_GB:.2f} GB')
#print(current,peak)
