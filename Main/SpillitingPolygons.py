# Annex 2: Splitting Polygons

import os
import json
from collections import OrderedDict

class GeoPoint:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class Contour:
    def __init__(self):
        self.noPoints = 0
        self.points = []

def separate_polygon(points):
    l1 = []
    l2 = []

    for gp in points:
        if gp.longitude < -47:  # Specify the splitting longitude here
            l1.append(gp)
        else:
            l2.append(gp)

    print("Points in L1:", len(l1))
    print("Points in L2:", len(l2))

    return l1, l2

def close_contour_if_needed(points):
    if len(points) >= 2 and points[0] != points[-1]:
        points.append(points[0])

IDWM_Contours = {}

def parse_coordinates(coordinates, contourID):
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
    contourID = None
    for line in lines:
        trimmed = line.strip()
        parts = trimmed.split()
        
        if len(parts) == 4:
            contourID = int(parts[0])
            if contourID not in IDWM_Contours:
                IDWM_Contours[contourID] = Contour()
            IDWM_Contours[contourID].noPoints = int(parts[2])
        elif len(parts) == 2 and contourID is not None:
            coordinates, point_no = parts[0], int(parts[1])
            longitude, latitude = parse_coordinates(coordinates, contourID)
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
        ("value", value),
        ("contour", int(contour_id))
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
