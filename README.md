# OOSA Assignment 2025

This contains the files needed for the 2025 OOSA assignment. The raw LVIS data can be downloaded from [here](https://lvis.gsfc.nasa.gov/Data/Data_Download.html), but files over the Pine Island Glacier have been provided on the teaching drive.  We will be using files from [Operation IceBridge](https://www.nasa.gov/mission_pages/icebridge/index.html), which bridged the gap between ICESat and ICESat-2 using aircraft.


## lvisClass.py

A class to handle LVIS data. This class reads in LVIS data from a HDF5 file, stores it within the class. It also contains methods to convert from the compressed elevation format and return attributes as numpy arrays. Note that LVIS data is stored in WGS84 (EPSG:4326).

The class is:

**lvisData**

The data is stored as the variables:

    waves:   Lidar waveforms as a 2D numpy array
    lon:     Longitude as a 1D numpy array
    lat:     Latitude as a 1D numpy array
    nWaves:  Number of waveforms in this file as an integer
    nBins:   Number of bins per waveform as an integer
    lZN:     Elevation of the bottom waveform bin
    lZ0:     Elevation of the top waveform bin
    lfid:    LVIS flight ID integer
    shotN:   LVIS shot number for this flight


The data should be read as:

    from lvisClass import lvisData
    lvis=lvisData(filename)


There is an optional spatial subsetter for when dealing with large datasets.

    lvis=lvisData(filename,minX=x0,minY=y0,maxX=x1,maxX=x1)

Where (x0,y0) is the bottom left coordinate of the area of interest and (x1,y1) is the top right.

To help choose the bounds, the bounds only can be read from the file, to save time and RAM:

    lvisData(filename,onlyBounds=True)


The elevations can be set on reading:

    lvis=lvisData(filename,seteElev=True)

Or later by calling the method:

    lvis.setElevations()

This will add the attribute:

    lvis.z:    # 2D numpy array of elevations of each waveform bin


The class includes the methods:

* setElevations(): converts the compressed elevations in to arrays of elevation, z.
* getOneWave(ind): returns one waveform as an array
* dumpCoords():    returns all coordinates as two numpy arrays
* dumpBounds():    returns the minX,minY,maxX,maxY


### Using the class in code

    # import and read bounds
    from lvisClass import lvisData
    bounds=lvisData(filename,onlyBounds=True)
      
    # set bounds
    x0=bounds[0]
    y0=bounds[1]
    x1=(bounds[2]-minX)/2+minX
    y1=(bounds[3]-minY)/2+minY
     
    # read data
    lvis=lvisData(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)
    lvis.setElevations()

This will find the data's bounds, read the bottom left quarter of it in to RAM, then set the elevation arrays. The data is now ready to be processed


## processLVIS.py

Includes a class with methods to process LVIS data. This inherits from **lvisData** in *lvisClass.py*. The initialiser is not overwritten and expects an LVIS HDF5 filename. The following methods are added:

* estimateGround():    Processes the waveforms and z arrays set above to populate self.zG
* reproject():         Reprojects horizontal coordinates
* findStats():         Used by estimateGround()
* denoise(thresh):     Used by estimateGround()

Some parameters are provided, but in all cases the defaults should be suitable. Further information on the signal processing steps and variable names can be found in [this](https://www.sciencedirect.com/science/article/pii/S0034425716304205) paper.


### Using the class in code

    from processLVIS import lvisGround
    lvis=lvisGround(filename)
    lvis.setElevations()
    lvis.estimateGround()

Note that the estimateGround() method can take a long time. It is recommended to perform time tests with a subset of data before applying to a complete file. This will produce an array of ground elevations contained in:

    lvis.zG


## lvisExample.py

Contains an example of how to call processLVIS.py on a 15th of a dataset. Intended for testing only. It could form the centre of a batch loop. It is a simple script with no options.


## handleTiff.py

Examples of how to write and read a geotiff embedded within a class. This is not a complete script, has no initialiser and so will not run in its current form.


* writeTiff(data):     writes raster data to a geotiff (*data* class needs modifying)
* readTiff(filename): reads the geotiff in *filename* to a numpy array with metadata

Note that geotiffs read the y axis from the top, so be careful when unpacking or packing data, otherwise the z axis will be flipped.

