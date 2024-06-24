# Geospatial-data-generator
#Project Overview
This project involves the processing and conversion of geographical data, specifically contour lines, from text files into various formats suitable for GIS applications. The workflow includes generating vector data from text files, splitting polygons based on specified criteria, and converting the data into raster formats. The project is divided into three main sections:

1_Vector Generation:
_Parsing text files containing geographical coordinates and converting them to JSON polygon types.
_Splitting Polygons: Dividing polygons based on specific longitude criteria and generating new JSON files.
2_Raster Generation: Converting the JSON files into GeoPackage and GeoJSON formats, and generating raster files from the geographical data.

#Requirements
Python Packages
To run the scripts, the following Python packages are required:
_json
_collections
_os
_pandas
_geopandas
_shapely
_numpy
_gdal
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

separate_polygon(): Splits polygons based on longitude values.
close_contour_if_needed(): Ensures that polygons are closed by appending the starting point to the end if needed.
Section 3: Raster Generation
This script converts the JSON files into a GeoPackage file and a GeoJSON file, making them readable in GIS applications like QGIS. It also generates raster files from the geographical data.

Key Functions:

geo_point_to_dict(): Converts GeoPoint objects to dictionaries.
contour_to_json(): Converts contour objects to JSON format.
read_values_file(): Reads contour values from a file.
generate_raster_files(): Generates raster files from latitude and longitude data.

#Running the Scripts
To run the scripts, follow these steps:

Vector Generation: Run the first script to parse text files and generate JSON files in the specified output directory.
Splitting Polygons: Run the second script to split the polygons and save the new JSON files.
Raster Generation: Run the third script to convert the JSON files into GeoPackage and GeoJSON formats and generate raster files.
Ensure that the input text files (LINES.txt and LINESIDX.DAT) and the output directories are correctly specified in the scripts before running them.
