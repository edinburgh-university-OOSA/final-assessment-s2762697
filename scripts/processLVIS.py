
'''Some example functions for processing LVIS data'''

#######################################

import numpy as np
from lvisClass import lvisData
from scipy.ndimage.filters import gaussian_filter1d
from pyproj import Transformer 

#######################################

class lvisGround(lvisData):
  ''' LVIS class with extra processing steps
  to allow it to found the ground over ice''' ##update

  #######################################################

  def reprojectLVIS(self,outEPSG):
    '''Reproject the data'''
    #set projections as direct strings
    inEPSG = "EPSG:4326"
    outEPSG = f"EPSG: {outEPSG}"
    #use transformer so dont deprecate with transform
    transformer = Transformer.from_crs(inEPSG, outEPSG, always_xy=True) #always long,lat order
    #reproject
    self.x, self.y = transformer.transform(self.lon, self.lat)

  #######################################################

  def estimateGround(self,sigThresh=5,statsLen=10,minWidth=3,sWidth=0.5):
    '''
    Processes waveforms to estimate ground
    Parameters are tailored for bare earth.
    '''
    # find noise statistics
    self.findStats(statsLen=statsLen)

    # set threshold
    threshold=self.setThreshold(sigThresh)

    # remove background
    self.denoise(threshold,minWidth=minWidth,sWidth=sWidth)

    # find centre of gravity of remaining signal
    self.CofG()


  #######################################################

  def setThreshold(self,sigThresh):
    '''
    Set a noise threshold
    '''
    threshold=self.meanNoise+sigThresh*self.stdevNoise
    return(threshold)

  #######################################################

  def CofG(self):
    ''' check
    Find centre of gravity of denoised waveforms
    sets this to an array of ground elevation
    estimates, zG
    '''

    # make new array 
    self.zG=np.full((self.nWaves),-999.0)   # fill with -999.0

    # loop over waveforms
    for i in range(0,self.nWaves):
      if(np.sum(self.denoised[i])>0.0):   # avoid empty waveforms (clouds etc)
        self.zG[i]=np.average(self.z[i],weights=self.denoised[i])  # centre of gravity


  ##############################################

  def findStats(self,statsLen=10):
    '''
    Finds standard deviation and mean of noise
    '''

    # make empty arrays
    self.meanNoise=np.empty(self.nWaves)
    self.stdevNoise=np.empty(self.nWaves)

    # determine number of bins to calculate stats over
    res=(self.z[0,0]-self.z[0,-1])/self.nBins    # range resolution
    noiseBins=int(statsLen/res)   # number of bins within "statsLen"

    # loop over waveforms
    for i in range(0,self.nWaves):
      self.meanNoise[i]=np.mean(self.waves[i,0:noiseBins])
      self.stdevNoise[i]=np.std(self.waves[i,0:noiseBins])


  ##############################################

  def denoise(self,threshold,sWidth=0.5,minWidth=3):
    '''
    Denoise waveform data
    '''

    # find resolution
    res=(self.z[0,0]-self.z[0,-1])/self.nBins    # range resolution

    # make array for output - intially stores 0's
    self.denoised=np.full((self.nWaves,self.nBins),0)

    # loop over number of waves
    for i in range(0,self.nWaves):
      #print("Denoising wave",i+1,"of",self.nWaves)   #delete

      # subtract mean background noise
      self.denoised[i]=self.waves[i]-self.meanNoise[i]

      # set all values less than threshold to zero
      self.denoised[i,self.denoised[i]<threshold[i]]=0.0

      # minimum acceptable width??
      # identify non-zero values
      binList=np.where(self.denoised[i]>0.0)[0]
      for j in range(0,binList.shape[0]):       # loop over waveforms
        if((j>0)&(j<(binList.shape[0]-1))):    # are we in the middle of the array?
          if((binList[j]!=binList[j-1]+1)|(binList[j]!=binList[j+1]-1)):  # are the bins consecutive?
            self.denoised[i,binList[j]]=0.0   # if not, set to zero

      # smooth with 1D guassian filter
      self.denoised[i]=gaussian_filter1d(self.denoised[i],sWidth/res)

