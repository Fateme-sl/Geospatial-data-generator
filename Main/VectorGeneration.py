Generating Polygons

# Section 1: Converting text files to JSON-polygon types

import json
from collections import OrderedDict
import os

class GeoPoint:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class Contour:
    def __init__(self):
        self.noPoints = 0
        self.points = []

IDWM_Contours = {}

def parse_coordinates(coordinates):
    latDeg = int(coordinates[0:2])
    latMin = int(coordinates[2:4])
    latSec = int(coordinates[4:6])
    NS = coordinates[6]
    lonDeg = int(coordinates[7:10])
    lonMin = int(coordinates[10:12])
    lonSec = int(coordinates[12:14])
    EW = coordinates[14]

    longitude = lonDeg + lonMin / 60.0 + lonSec / 3600.0

    if EW == "W":
        longitude = -longitude    

    latitude = latDeg + latMin / 60.0 + latSec / 3600.0

    if NS == "S":
        latitude = -latitude

    return longitude, latitude

def parse_lines(lines):
    for line in lines:
        trimmed = line.strip()
        parts = trimmed.split()

        if len(parts) == 4:  # index reference 10001 1 5745 0
            contourID = int(parts[0])
            first = int(parts[1])
            last = int(parts[2])
            dummy = int(parts[3])

            if contourID not in IDWM_Contours:
                IDWM_Contours[contourID] = Contour()

            IDWM_Contours[contourID].noPoints = last
        elif len(parts) == 2:  # points
            coordinates, point_no = parts[0], int(parts[1])

            if contourID not in IDWM_Contours:
                IDWM_Contours[contourID] = Contour()

            longitude, latitude = parse_coordinates(coordinates)
            IDWM_Contours[contourID].points.append(GeoPoint(longitude, latitude))

def geo_point_to_dict(geo_point):
    return OrderedDict([("type", "Point"), ("coordinates", [geo_point.longitude, geo_point.latitude])])

def contour_to_json(contour, value):
    geometry = OrderedDict([
        ("type", "Polygon"),
        ("coordinates", [[(point.longitude, point.latitude) for point in contour.points]])
    ])
    feature = OrderedDict([
        ("type", "Feature"),
        ("geometry", geometry),
        ("contour_id", contour_id),
        ("value", value)
    ])
    
    return json.dumps(feature, indent=2)

def read_values_file(file_path):
    values = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            contour_id = parts[0]
            value = " ".join(parts[1:3])
            values[int(contour_id)] = value
    return values

file_path = "path_to_LINES.txt"

with open(file_path, "r") as file:
    lines = file.readlines()

parse_lines(lines)

values_file_path = "path_to_LINESIDX.DAT"
contour_values = read_values_file(values_file_path)

output_directory = "path_to_output_directory/JSONs"
os.makedirs(output_directory, exist_ok=True)

for contour_id, contour in IDWM_Contours.items():
    json_data = contour_to_json(contour, contour_values.get(contour_id, 0))  # Assign a default value of 0 if not found in the file
    output_file_path = os.path.join(output_directory, f"contour_{contour_id}.json")

    with open(output_file_path, "w") as output_file:
        output_file.write(json_data)
  
print("done")

# Section 2: Convert the JSON files to one GPKG file

import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

data = []

json_files_directory = "path_to_output_directory/JSONs"

for file_name in os.listdir(json_files_directory):
    if file_name.endswith(".json"):
        file_path = os.path.join(json_files_directory, file_name)
        with open(file_path, "r") as file:
            json_data = json.load(file)
            data.append(json_data)

df = pd.DataFrame(data)

geometry = [shape(geom) for geom in df['geometry']]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

output_directory = "path_to_output_directory/GPKG"
os.makedirs(output_directory, exist_ok=True)
output_gpkg_file = os.path.join(output_directory, "output_file.gpkg")
gdf.to_file(output_gpkg_file, driver="GPKG")

print("done")

# Section 3: Convert the JSON files to one JSON or GeoJSON file

# Convert JSON files to one JSON file

json_data_list = []

for file_name in os.listdir(json_files_directory):
    if file_name.endswith(".json"):
        file_path = os.path.join(json_files_directory, file_name)
        with open(file_path, "r") as file:
            json_data = json.load(file)
            json_data_list.append(json_data)

output_json_file = "output_file.json"
with open(output_json_file, "w") as file:
    json.dump(json_data_list, file, indent=2)

# Convert JSON files to one GeoJSON file

data = []

for file_name in os.listdir(json_files_directory):
    if file_name.endswith(".json"):
        file_path = os.path.join(json_files_directory, file_name)
        with open(file_path, "r") as file:
            json_data = json.load(file)
            data.append(json_data)

df = pd.DataFrame(data)

geometry = [shape(geom) for geom in df['geometry']]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

output_geojson_file = "output_file.geojson"
gdf.to_file(output_geojson_file, driver="GeoJSON")

print("done")
