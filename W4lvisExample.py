
'''An example of how to use the LVIS python scripts'''

# import libraries
#from lvisClass import lvisData
import h5py
from pyproj import Transformer
from matplotlib import pyplot as plt
from glob import glob

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


  #def reprojectBounds(self, outEPSG):
  #  '''Reproject file boundaries'''
  #  #set projections as direct strings
  #  inEPSG = "EPSG:4326"
  #  outEPSG = f"EPSG: {outEPSG}"
  #  ######define bounds
  #  self.bounds = [[self.lon[0], self.lon[0]]]
#
  #  #use transformer so dont deprecate with transform
  #  transformer = Transformer.from_crs(inEPSG, outEPSG, always_xy=True) #always long,lat order
  #  #reproject 
  #  self.bounds[0,2],self.bounds[1,3] = transformer.transform(
  #    inEPSG,outEPSG, self.bounds[0,2], self.bounds[1,3])
  #  plt.plot(self.bounds[0,2], self.bounds[1,3])
  #  plt.show()

  def plotSingleWave(self, save_path='Waveform.png'):
    '''Plot single waveform and exports as a png'''
    #get rid of baseline noise
    #for i in enumerate(self.waves):
    #  if (self.waves == 0):
    #    slice_index = i
    #    break
    #filtered_wave = self.waves[:slice_index]
    #filtered_elevation = self.z[:slice_index]       

 #lvis.z[24]
    #plt.xlabel("Waveform return")
    #plt.ylabel("Elevation (m)")
    #plt.plot(filtered_wave, filtered_elevation, c='purple')    #waveform  at index 20  #update
    #plt.savefig(save_path, bbox_inches='tight')
    #print(f'Waveform has been saved to {save_path}')
    #plt.show()

    ##lvis.z[24]
    plt.xlabel("Waveform return")
    plt.ylabel("Elevation (m)")
    plt.plot(self.waves[24], self.z[24], c='purple')    #waveform  at index 20  #update
    plt.savefig(save_path, bbox_inches='tight')
    print(f'Waveform has been saved to {save_path}')
    plt.show()

  def makeDEM(self, resolution, outName):
    '''convert data to a goetiff (from tiffExample.py)'''
    writeTiff(self.zGravity, self.x, self.y, resolution, filename=outName, epsg=3031)
    return 

##########################################

if __name__=="__main__":
  '''Main block'''

##########################################
  #for looping through all files
  #filelist_2009 = glob('/geos/netdata/oosa/assignment/lvis/2009/*.h5')  #only.h5 files
  #print(filelist_2009)
  #filelist_2015 = glob('/geos/netdata/oosa/assignment/lvis/2015/*.h5')  #only.h5 files
  #print(filelist_2015)

  #filename='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_058456.h5'  #pine yay 
  #filename='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_055102.h5' # doesnt work?
  filename='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_071909.h5'  #over ocean
  #filename='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_058456.h5' #doesnt work


##############################################
  #find bounds
  #b=plotLVIS(filelist_2009[0],onlyBounds=True)    #first index in list
  b=plotLVIS(filename,onlyBounds=True)    #first index in list
  #b=plotLVIS(filelist_2015,onlyBounds=True)
  
  #loop for subdivisions 
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

      #all inside loop
      # read in all data within our spatial subset
      lvis=plotLVIS(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)
      #lvis=plotLVIS(filelist_2009[0],minX=x0,minY=y0,maxX=x1,maxY=y1)

      # check that it contains some data
      if(lvis.nWaves==0):
        continue

      #reproject the data
      lvis.reprojectLVIS(3031)
      #lvis.reprojectBounds(3031)

      #set elevation
      lvis.setElevations() #old function from lvisclass
      lvis.estimateGround()     #find ground
  
  ###outside loop
  #print(lvis.zGravity)
  tiffName = "lvisDEM_PIG.x"+str(x0)+".y."+str(y0)+".tif"   #filename with bands
  #lvis.makeDEM(100, tiffName)       #resolution 

  ###call function to plot single waveform
  lvis.plotSingleWave()
  ###check bounds
  print(f'Subset bounds{x0, y0} to {x1, y1}')

  print(f'Each geotiff is split into {subset_size} x {subset_size} tiles') 
  #print(lvis.waves)
  #print(f"There are {len(lvis.waves)} variables")????

  # denoise test
  lvis.findStats()
  threshold=lvis.meanNoise+5*lvis.stdevNoise
  lvis.denoise(threshold)
  print(lvis.findStats)
  #print(lvis.denoise)
