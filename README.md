## OOSA Final Assignment.

This library uses the raw Land, Vegetetaion and Ice Sensor (LVIS) data ([link](https://lvis.gsfc.nasa.gov/Data/Data_Download.html)) via _geosnetdata_, from Operation IceBridge to process and create raster DEMs from the 20th October 2009 and 17th October 2015.

**The repository is organised as follows:**

```
│── source/
│   │── lvisClass.py
│   │── processLVIS.pyV
│   │── handleTiff.py
│── DATA 2009/
│── Data2015/
│── Outputs/
│── Task1.py
│── Task2.py
│── Task3.py
│── README.md
```
-	**Source:** Contains multiple files that are required to complete the specified tasks.
-	**Data2009:** A folder where the 2009 tiled rasters are stored when being processed.
-	**Data 2015:** A folder where the 2015 tiled rasters are stored when being processed.
-	**Outputs:** A folder where the final outputs are stored. This includes the waveform.png, single file DEM and full DEMs for both 2009 and 2015.
-	**TasksX** run each specifed task.
-	README file.
-----
### Libraries Required: 
The follwowing libraries are required for the scripts to run:
-	NumPy: For array operations such as data cleaning, transformation and aggregation.
-	h5py: to read and write HDF5 files. 
-	Matplotlib: For formatting and displaying the plots.
-	os: For file system operations.
-	rasterio (and rasterio.merge): For reading, writing and handling rasters.
-	osgeo (gdal and osr): For handling geotiff data and managing projections.
-	pyproj (Transformer): For coordinate system transformations.
-	Glob (Glob): For iterating through multiple files in a folder.
-	argparse: For handling command line options.
-	Tracemalloc: For tracking memory during script use.

To install:
```
    pip install GDAL numpy h5py matplotlib rasterio pyproj
```
-----------
### Running The Code:
**Install the github repo**
To clone the repository:
```
    git clone etc...
```
**Task 1:**

To run:
```
    python Task1.py --i (chosen index) --output (Example.png)
```  
1. This script reads the specifed file and creates a plot of _one waves'_ full LiDAR return data (amplitude). 
2. If chosen index contains data, this saves the plot to the Output folder.
3. pic of output?

**Task 2:**

To run:
```
    python Task2.py --res (res) --tiff_output (Example.tif)
```
1. This script creates subset tiles and loops through (for one file) and converts the tiles into rasters of a chosen resolution.
2. These rasters are stored in a folder (Data2009) and then merged into one TIF. file.
3. 
4.

  
**Task 3:**

**Task 4:**

**Task 5:**


----------------
References:!?
==============================
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

