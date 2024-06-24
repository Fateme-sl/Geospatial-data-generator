# Geospatial-data-generator
#Project Overview:

Telecommunication companies often need to analyze geographical data to optimize their services. This project automates the conversion of raw telecommunication flat data into visual polygons and rasters, facilitating better spatial analysis. This involves the processing and conversion of geographical data, specifically contour lines, from text files into various formats suitable for GIS applications.

Key features of this project include:
- Reading telecommunication data from a flat file.
- Generating geographical polygons and rasters from coordinate data.
- Saving the output in a suitable format for easy visualization and analysis in GIS applications.


The project is divided into the following parts:
- Vector Generation:
  - Section 1: Converting Text Files to JSON-Polygons
    This script parses text files to create JSON files representing polygons. Each polygon's points are derived from given coordinates, and values are assigned based on an index file.
  - Section 2: Converting JSON Files to GPKG
    This script reads multiple JSON files containing polygon data and combines them into a single GeoPackage (GPKG) file.
  - Section 3: Converting JSON Files to Single JSON or GeoJSON
    This script aggregates multiple JSON files into a single JSON file or GeoJSON file, making it easier to handle and visualize in GIS software like QGIS.







- Splitting Polygons:
  This script splits polygons that are attached based on a specified longitude. It ensures that each resulting polygon is properly closed and writes them to JSON files.

- Raster Generation:
  This script generates raster files from flat files containing pixel sizes, coordinates, and values. It uses GDAL to create GeoTIFF files and handles necessary transformations and compressions.






#Requirements

Python Packages

To run the scripts, the following Python packages are required, as mentioned in the requirements.txt:

- json
- collections
- os
- osgeo
- pandas
- geopandas
- shapely
- numpy
- gdal



#Installation
You can install the necessary Python packages using pip. Run the following command in your terminal:
"pip install json pandas geopandas shapely numpy gdal"



#Script Descriptions
_Section 1: Vector Generation
This script reads geographical data from text files, parses the coordinates, and converts them into JSON polygon types. It also assigns values to each polygon based on their index.

Key Functions:

parse_coordinates(): Converts coordinate strings to longitude and latitude values.
parse_lines(): Parses lines from the text files and creates contour objects.
contour_to_json(): Converts contour objects to JSON format.
read_values_file(): Reads values from a file and assigns them to contours.

_Section 2: Splitting Polygons
This script processes the JSON files generated in the previous step, splits polygons based on specified longitude criteria, and saves the split polygons into new JSON files.

Key Functions:

separate_polygon(): 
Splits polygons based on longitude values.

close_contour_if_needed():
Ensures that polygons are closed by appending the starting point to the end if needed.

Section 3: Raster Generation
This script converts the JSON files into a GeoPackage file and a GeoJSON file, making them readable in GIS applications like QGIS. It also generates raster files from the geographical data.

Key Functions:

geo_point_to_dict(): Converts GeoPoint objects to dictionaries.
contour_to_json(): Converts contour objects to JSON format.
read_values_file(): Reads contour values from a file.
generate_raster_files(): Generates raster files from latitude and longitude data.



#Running the Scripts
To run the scripts, follow these steps:

- Vector Generation:
  Run the following command in your terminal
  - python VectorGeneration.py


- Splitting Polygons:
   Run the following command in your terminal
  - python SpillitingPolygon.py





- Raster Generation:
  Run the following command in your terminal
  - python RasterGeneration.py



#Input data format:
- For Vector Generation, our input data should be two .DAT files with the following formats:
  - LINES.DAT: This contains 3 columns for each polygon index, which is specified in the beginning of each series of coordinates as a header line, the first column is the Latitude, the second is the Longitude, and the third is the point number in the corresponding polygon.
  - LINESIDX.DAT: This has 2 columns, the first column is the index of the polygon, the second column is the corresponding value of the polygon.
  Ensure that the input text files (LINES.txt and LINESIDX.DAT) and the output directories are correctly specified in the scripts before running them.

- for Raster Generation, our input format would be:
  - Lat.txt: Latitude for each pixel.
  - Long.txt: Longitude for each pixel.
  - Value.txt: value of each pixel.
  we also specify the pixel size of our raster data.
