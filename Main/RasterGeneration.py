#This is the script for the georeferencing of the Recommendation
# "Monthly and annulat total columnar water vbapour exceedance probability (%)
# (IWVC)(Rec.ITU-R P.836)"
# Most of the commands are explained

import numpy as np #Provides fast and efficient operation on arrays of homogeneous data, it is used to work with N-dimensional arrays
import os #Provides functions for interacting with the operative system
import glob #Finds the pathnames matching a specified pattern, returning results in arbitrary order
from osgeo import gdal, gdal_array, osr #offers the possibility to work with arrays, spatial reference and as a translator library for raster and vector geospatial data format
import sys

drc = os.getcwd() # select the emplacement of this script to facilitate the paths, if the script is moved to another folder

l = open ('TOPOLAT.txt', "r") # select the latitude text file and opens it in "read" mode
f = open ('TOPOLON.txt', "r") # select the longitude text file and opens it in "read" mode
d = open ('TOPO_0DOT5.txt',"r") # select the dataset text file and opens it in "read" mode
lon = f.read().split('\n') # reads the longitude file, while dividing each line 
lat = l.read().split('\n')
data = d.read().split('\n')
while lon[-1] == '': # set a condition: "if the last line is empty"
     lon.remove(lon[-1]) # removes the last line (if there was nothing)
while lat[-1] == '':
     lat.remove(lat[-1]) 
while data[-1] == '': 
     data.remove(data[-1])
for i in range(0,len(lon)): # select each line individually (from 0 to the last line (len(lon) being the lenght of the line)      
     lon[i]=lon[i].split() # in each line, separates every character individually, when a "space" occurs
     lat[i]=lat[i].split()
     data[i] = data[i].split()
     lon[i].pop(-2) # removes the values not necessary (360° is already equal to 0° and need to get removed
     lon[i].pop(-1) # the two last and first values are removed, as the text files contains 1 values unecessary on each part
     lon[i].pop(0) # and the 360.
     lat[i].pop(-2)# Note that the pop(-2) has to be first, otherwise, the command must be pop(-1) twice, to avoid removing the wrong value
     lat[i].pop(-1)
     lat[i].pop(0)
     data[i].pop(-2)
     data[i].pop(-1)
     data[i].pop(0)
lat.pop(0) # for the same reason, latitude contains values for -90.5 and 90.5 that need removal on all the files
lat.pop(-1)
lon.pop(0)
lon.pop(-1)
data.pop(0)
data.pop(-1)
         
t = open("monthly_total_columnar_content.csv","r") # open the cvs containing the metadata in "read" mode
csv = t.read().split('\n') #cf. line 17
while csv[-1] == ('\n'): # cf. line 20
     csv.remove(csv[-1])

head = csv[0].split(';') # like in line 27, the csv file is split, but the elements here are delimited by ";"
info = csv[1].split(';')

     

a = int(float(len(lon[0]))/2) # select the middle of the longitude (180)
A=[0]*len(lon) # creates an empty list "A" with len(lon) rows, first half of values (0 - 180)
Alon=[0]*len(lon) # creates an empty list for the longitude, latitude is ignored because only a horizontal motion will be applied
B=[0]*len(lon) # creates an empty list "B" with len(lon) rows, for the second half of values (180-360)
Blon=[0]*len(lon)
BA=[0]*len(data) # Creates a new list for the new list, row = number of rows in data
BAlon=[0]*len(data)
BAlat = lat # as the latitude don't need modification, the variable can already be set 

for i in range(0, len(lon)): # for each one of this row
          A[i] = Alon[i] = [0]*len(lon[0][:(a+1)]) # creates columns up to the value "180" (a + 1 because it neglicted the last value (180) otherwise)
          A[i] = data[i][:(a+1)] #fill the new list (half of the lon) with the fieldstrenghs values
          Alon[i] = lon[i][:(a+1)]
          B[i] = Blon[i] = [0]*len(lon[0][a:])# creates columns from "180" up to the end (360) 
          B[i] = data[i][a:] # fill the new list with (other half of the lon) with the fieldstrenghs values
          Blon[i] = lon[i][a:]
          for j in range (0, len(Blon[i])):
               Blon[i][j] = float(Blon[i][j]) - 360 # transform B values in negative
          BA[i] = BAlon[i] = [0]*len(lon[i]) # cf. line 66
          BA[i] = B[i] + A[i] # fill the new list with the values of B list followed by A list
          BAlon[i] = Blon[i] + Alon[i]
####
arr = np.array(BA) #change de type of datas from list to np.array
latmid = np.array(BAlat)
lonmid = np.array(BAlon)
array = arr.astype(np.float) # change the type of datas from str to float, individually
latfin = latmid.astype(np.float)
lonfin = lonmid.astype(np.float)
xmin,ymin,xmax,ymax = [lonfin.min(),latfin.min(),lonfin.max(),latfin.max()]
    # find the min and max for lon and lat
nrows,ncols = np.shape(array) # calculate the size of the array, getting the number of rows and columns
xres = ((xmax - xmin)/float(ncols-1)) # measure the resolution of x axis. the -1 is because each point is the center of the pixel and not the border
yres = ((ymax - ymin)/ float(nrows-1)) # therefore, the 2x half pixels located outside oof the map boundaries aren't taking in acount and need this correction

geotransform =((xmin - (xres/2)),xres,0,(ymax + (yres/2)) ,0, -yres) # Determine the Upper Left Corner, and the lateral variation (+xres) and vertical (-yres)
base = os.path.splitext(d.name)[0] # from the path, select the name of the dataset
base = base + '.tif' # create the name of the futur tif file
GeoTIFF_interm = ('GeoTIFF_interm')
if not os.path.exists(GeoTIFF_interm): #states that if the folder "GeoTIFF_interm" doesn't exist
     os.makedirs(GeoTIFF_interm) # it is created
output_raster = gdal.GetDriverByName('GTiff').Create(GeoTIFF_interm +'\\'+ base,ncols, nrows, 1 ,gdal.GDT_Float32) # get information of the output_raster
output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
srs = osr.SpatialReference()                 # Establish its coordinate encoding
srs.ImportFromEPSG(4326)                     # This one specifies WGS84 lat long.
                                                  # Anyone know how to specify the 
                                                  # IAU2000:49900 Mars encoding?
output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system 
                                                                  # to the file
output_raster.SetMetadataItem("AREA_OR_POINT",'Point') # set the metadata "AREA_OR_POINT" to "Point"
for i in range (0, len(head)): # for each field of the metadata individually
     output_raster.SetMetadataItem(head[i],info[i]) # link each field to the definition on the csv file
output_raster.GetRasterBand(1).WriteArray(array)   # Writes  array to the raster
          
output_raster.FlushCache()




l = open (drc + '\P_836_Maps_annual\\Surface Water Vapor Density\RHO Annual Maps\lat1dot125.txt', "r") # cf. 14
f = open (drc + '\P_836_Maps_annual\\Surface Water Vapor Density\RHO Annual Maps\lon1dot125.txt', "r") 

lon = f.read().split('\n') # cf. 17
lat = l.read().split('\n')
while lon[-1] == '': # cf. 20
     lon.remove(lon[-1])
while lat[-1] == '':
     lat.remove(lat[-1]) 
for i in range(0,len(lon)): # cf. 26
     lon[i]=lon[i].split() 
     lat[i]=lat[i].split()
     lon[i].pop(-1) # remove the last value of lat and lon (the 360, equivalent to the 0)
     lat[i].pop(-1)




for subdir in glob.glob(drc + '\\*' + '\\*'): # Select all the subfolders (second level) in the drc
     for subdir2 in glob.glob(subdir + '\\*'): # Select all the subfolders of each subdir
          if os.path.isdir(subdir2) == True: # state if subdir2 is a directory (and not a file)
               os.chdir(subdir2) # the folder "subdir2" becomes the new working directory
               for p in glob.glob('*.txt'): # select all text files in the directory naming them "p"

                    d = open (p,"r") #cf. 14
                    data = d.read().split('\n') # split the data with all the "break line"
                    while data[-1] == '': # remove the last lines of txt file if they are empty
                         data.remove(data[-1]) # cf. 21             
                    for i in range(0,len(lon)): # separate the lines individually        
                         data[i]=data[i].split()
                         data[i].pop(-1) #remove the last (blank) line of every file (done for lat and lon in line 126/127

                    a = int(len(lon[0])/2) # cf. 56
                    A=[0]*len(lon) # creates an empty list "A" with len(lon) rows, frist half of values (0 - 180)
                    Alon=[0]*len(lon)
                    B=[0]*len(lon) # creates an empty list "B" with len(lon) rows, for the second half of values (180-360)
                    Blon=[0]*len(lon)
                    BA=[0]*len(data) # Creates a new list for the new list, row = number of rows in data
                    BAlon=[0]*len(data)
                    BAlat = lat

                    for i in range(0, len(lon)): # for each one of this row
                         A[i] = Alon[i] = [0]*len(lon[0][:(a+1)]) # creates columns up to the value "180" (a + 1 because it neglicted the last value of a otherwise)
                         A[i] = data[i][:(a+1)] #fill the new list (half of the lon) with the fieldstrenghs values
                         Alon[i] = lon[i][:(a+1)]
                         B[i] = Blon[i] = [0]*len(lon[0][a:])# creates columns from "180" up to the end (360) 
                         B[i] = data[i][a:] # fill the new list with (other half of the lon) with the fieldstrenghs values
                         Blon[i] = lon[i][a:]
                         for j in range (0, len(Blon[i])):
                              Blon[i][j] = float(Blon[i][j]) - 360 # transform B values in negative
                         BA[i] = BAlon[i] = [0]*len(lon[i])
                         BA[i] = B[i] + A[i] # fill the new list with the values of B list followed by A list
                         BAlon[i] = Blon[i] + Alon[i]


                    arr = np.array(BA) #change de type of datas from list to np.array
                    latmid = np.array(BAlat)
                    lonmid = np.array(BAlon)
                    array = arr.astype(np.float) # change the type of datas from str to float
                    latfin = latmid.astype(np.float)
                    lonfin = lonmid.astype(np.float)
                    xmin,ymin,xmax,ymax = [lonfin.min(),latfin.min(),lonfin.max(),latfin.max()]
                    ##     # find the min and max for lon and lat
                    nrows,ncols = np.shape(array)
                    xres = ((xmax - xmin)/float(ncols-1)) # measure the resolution of x axis. the -1 is for the -180 added
                    yres = ((ymax - ymin)/ float(nrows-1))

                    geotransform =((xmin - (xres/2)),xres,0,(ymax + (yres/2)) ,0, -yres) # neither is taken in acount (values usually -180, 90)
                    base = os.path.splitext(p)[0]
                    base = base + '.tif' # create the name of the futur tif file
                    GeoTIFF_interm = ('GeoTIFF_interm')
                    if not os.path.exists(GeoTIFF_interm):
                         os.makedirs(GeoTIFF_interm)
                    output_raster = gdal.GetDriverByName('GTiff').Create(GeoTIFF_interm +'\\'+ base,ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
                    output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
                    srs = osr.SpatialReference()                 # Establish its coordinate encoding
                    srs.ImportFromEPSG(4326)                     # This one specifies WGS84 lat long.
                                                                      # Anyone know how to specify the 
                                                                 # IAU2000:49900 Mars encoding?
                    output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system 
                                                                       # to the file
                    output_raster.SetMetadataItem("AREA_OR_POINT",'Point')
                    for i in range (0, len(head)): # for each field of the metadata individually
                         output_raster.SetMetadataItem(head[i],info[i]) 
                    output_raster.GetRasterBand(1).WriteArray(array)   # Writes my array to the raster
                    
                    output_raster.FlushCache()

os.chdir(drc) # Changes the current working directory
GeoTIFF_final = 'GeoTIFF_final' # Creates the folder "GeoTIFF_final" if not already existing
if not os.path.exists(GeoTIFF_final):
     os.makedirs(GeoTIFF_final)
os.chdir(drc +'\\GeoTIFF_interm') #changes the directory to take the interm files
for p in glob.glob ('*.tif'): # select all the ".tif" files
     os.chdir(drc +'\\GeoTIFF_interm')
     base = os.path.splitext(p)[0] # isolate the name of the file
     gtif = gdal.Open(p) #uses gdal for opening the file, as it is a tif file
     inf = gdal.Info(gtif) # get the information about the map
     os.chdir(drc + '\\GeoTIFF_final')
     translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -co COMPRESS=DEFLATE")) #use the parsecommnand to write the requesto for the translation (tiling, Blocksize, compression)
     gdal.Translate(base + "_f.tif", gtif, options = translateoptions) # Apply the translation with the resquested defined before


os.chdir(drc + '\\GeoTIFF_final')

for p in glob.glob('*.tif'):
     gtif = gdal.Open(p,1)
     inf = gdal.Info(p)
     print (inf)
     gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE') # select the compression mode of the overview
     gdal.SetConfigOption('GDAL_TIFF_OVR_BLOCKSIZE', '256') # defines the blocksize
     gtif.BuildOverviews("NEAREST", [2,4,8,16,32]) # build 5 overview using "nearest" mode, with a ratio of 2 between each
     inf = gdal.Info(p)
     print (inf) # print the information about the gtif


for subdir in glob.glob(drc + '\\*' + '\\*'):
     for subdir2 in glob.glob(subdir + '\\*'):         
          if os.path.isdir(subdir2 + '\\GeoTIFF_interm') == True:
               os.chdir(subdir2)
               GeoTIFF_final = 'GeoTIFF_final'
               if not os.path.exists(GeoTIFF_final):
                    os.makedirs(GeoTIFF_final)
               os.chdir(subdir2 +'\\GeoTIFF_interm')
               for p in glob.glob ('*.tif'):
                    os.chdir(subdir2 +'\\GeoTIFF_interm')
                    base = os.path.splitext(p)[0]
                    gtif = gdal.Open(p)
                    inf = gdal.Info(gtif)
                    os.chdir(subdir2 + '\\GeoTIFF_final')
                    translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -co COMPRESS=DEFLATE"))
                    gdal.Translate(base + "_f.tif", gtif, options = translateoptions)

               for p in glob.glob('*.tif'):
                    gtif = gdal.Open(p,1)
                    inf = gdal.Info(p)
                    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
                    gdal.SetConfigOption('GDAL_TIFF_OVR_BLOCKSIZE', '256')
                    gtif.BuildOverviews("NEAREST", [2,4,8,16,32])
                    inf = gdal.Info(p)
                    print (inf)

sys.exit()

