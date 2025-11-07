#!/usr/bin/env python3
"""
Create a 448m hexagonal building at specified location
Based on floor area data from Excel
"""
import pandas as pd
import math
import xml.etree.ElementTree as ET

# Read Excel file
excel_file = '청라_층별_넓이.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet1')

print("=" * 80)
print("Creating 448m Hexagonal Building")
print("=" * 80)

# Building parameters
CENTER_LAT = 37.532848
CENTER_LON = 126.634094
TOTAL_HEIGHT = 448.0  # meters

# Process floor data
floors = []
for idx, row in df.iterrows():
    floor_num = str(row['층'])
    area_sqm = row['면적(미터제곱)']
    
    floors.append({
        'floor': floor_num,
        'area': area_sqm
    })

total_floors = len(floors)
print(f"\nTotal floors: {total_floors}")
print(f"Target height: {TOTAL_HEIGHT}m")

# Calculate height per floor
# 448m / 34 floors = 13.176m per floor
floor_height = TOTAL_HEIGHT / total_floors
print(f"Height per floor: {floor_height:.2f}m")

# Create KML structure
def create_hexagon_from_area(center_lat, center_lon, area_sqm):
    """
    Create hexagon coordinates from center point and area
    Regular hexagon: Area = (3√3/2) × side²
    side = √(2×Area / (3√3))
    """
    # Calculate side length from area
    side_length_m = math.sqrt(2 * area_sqm / (3 * math.sqrt(3)))
    
    # Convert side length to degrees (approximate)
    # 1 degree latitude ≈ 111,000m
    # 1 degree longitude ≈ 111,000m × cos(latitude)
    lat_per_meter = 1.0 / 111000.0
    lon_per_meter = 1.0 / (111000.0 * math.cos(math.radians(center_lat)))
    
    # Radius of circumscribed circle = side_length
    radius_m = side_length_m
    
    # Create 6 points of hexagon (starting from top, going clockwise)
    coords = []
    for i in range(6):
        angle = math.radians(90 - 60 * i)  # Start from top (90°), go clockwise
        lat = center_lat + radius_m * math.sin(angle) * lat_per_meter
        lon = center_lon + radius_m * math.cos(angle) * lon_per_meter
        coords.append((lon, lat))
    
    # Close the polygon
    coords.append(coords[0])
    
    return coords

# Load existing KML
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

# Register namespace
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Find document
document = root.find('.//kml:Document', ns)

print("\n" + "=" * 80)
print("Creating floor polygons...")
print("=" * 80)

# Create Folder for the building
folder = ET.Element('{http://www.opengis.net/kml/2.2}Folder')
folder_name = ET.SubElement(folder, '{http://www.opengis.net/kml/2.2}name')
folder_name.text = "청라 신축 타워 (448m)"

# Create each floor as a separate polygon
cumulative_height = 0.0

for floor_data in floors:
    floor_num = floor_data['floor']
    area = floor_data['area']
    
    # Calculate floor base and top heights
    base_height = cumulative_height
    top_height = cumulative_height + floor_height
    cumulative_height = top_height
    
    # Create hexagon coordinates
    hex_coords = create_hexagon_from_area(CENTER_LAT, CENTER_LON, area)
    
    # Create Placemark
    placemark = ET.SubElement(folder, '{http://www.opengis.net/kml/2.2}Placemark')
    
    # Name
    name = ET.SubElement(placemark, '{http://www.opengis.net/kml/2.2}name')
    name.text = f"청라 신축 타워 - {floor_num}층 ({area:.1f}㎡)"
    
    # Description
    desc = ET.SubElement(placemark, '{http://www.opengis.net/kml/2.2}description')
    desc.text = f"층: {floor_num}\n면적: {area:.2f}㎡\n높이: {base_height:.1f}m - {top_height:.1f}m"
    
    # Style
    style = ET.SubElement(placemark, '{http://www.opengis.net/kml/2.2}Style')
    line_style = ET.SubElement(style, '{http://www.opengis.net/kml/2.2}LineStyle')
    line_color = ET.SubElement(line_style, '{http://www.opengis.net/kml/2.2}color')
    line_color.text = 'ffffffff'  # White outline
    line_width = ET.SubElement(line_style, '{http://www.opengris.net/kml/2.2}width')
    line_width.text = '2'
    
    poly_style = ET.SubElement(style, '{http://www.opengis.net/kml/2.2}PolyStyle')
    poly_color = ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}color')
    # Gold color for super tall building
    poly_color.text = 'ff00d4ff'  # Opaque gold
    poly_fill = ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}fill')
    poly_fill.text = '1'
    poly_outline = ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}outline')
    poly_outline.text = '1'
    
    # Polygon
    polygon = ET.SubElement(placemark, '{http://www.opengis.net/kml/2.2}Polygon')
    extrude = ET.SubElement(polygon, '{http://www.opengis.net/kml/2.2}extrude')
    extrude.text = '1'
    altitude_mode = ET.SubElement(polygon, '{http://www.opengis.net/kml/2.2}altitudeMode')
    altitude_mode.text = 'relativeToGround'
    
    outer_boundary = ET.SubElement(polygon, '{http://www.opengis.net/kml/2.2}outerBoundaryIs')
    linear_ring = ET.SubElement(outer_boundary, '{http://www.opengis.net/kml/2.2}LinearRing')
    coordinates = ET.SubElement(linear_ring, '{http://www.opengis.net/kml/2.2}coordinates')
    
    # Format coordinates with altitude
    coord_strings = []
    for lon, lat in hex_coords:
        coord_strings.append(f"{lon:.7f},{lat:.7f},{top_height:.1f}")
    
    coordinates.text = '\n' + ' '.join(coord_strings) + '\n'
    
    print(f"  Floor {floor_num:>5}: {area:>10.2f}㎡, Height: {base_height:>6.1f}m - {top_height:>6.1f}m")

# Add folder to document
document.append(folder)

# Save
tree.write('cheongna_buildings_2.5km_perfect.kml', encoding='utf-8', xml_declaration=True)

print("\n" + "=" * 80)
print("✓ Building created successfully!")
print(f"  Location: ({CENTER_LAT}, {CENTER_LON})")
print(f"  Total height: {TOTAL_HEIGHT}m")
print(f"  Total floors: {total_floors}")
print(f"  Floor height: {floor_height:.2f}m")
print(f"  Shape: Regular hexagon (각 층별 면적에 맞춤)")
print(f"  Color: Gold (448m super tall building)")
print("=" * 80)
