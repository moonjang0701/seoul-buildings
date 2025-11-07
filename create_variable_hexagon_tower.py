#!/usr/bin/env python3
"""
Create a 448m hexagonal tower with variable floor areas
Each floor is a separate polygon with different sized hexagon
Location: 37.532848, 126.634094
"""
import pandas as pd
import math
import xml.etree.ElementTree as ET

print("=" * 80)
print("Creating 448m Variable Hexagon Tower (층별 면적 다름)")
print("=" * 80)

# Read Excel file
excel_file = '청라_층별_넓이_수정.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet1')

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
floor_height = TOTAL_HEIGHT / total_floors

print(f"\n건물 정보:")
print(f"  위치: ({CENTER_LAT}, {CENTER_LON})")
print(f"  총 높이: {TOTAL_HEIGHT}m")
print(f"  총 층수: {total_floors}층")
print(f"  층당 높이: {floor_height:.2f}m")

def create_hexagon_from_area(center_lat, center_lon, area_sqm):
    """
    Create hexagon coordinates from center point and area
    Regular hexagon: Area = (3√3/2) × side²
    Therefore: side = √(2×Area / (3√3))
    """
    # Calculate side length from area
    side_length_m = math.sqrt(2 * area_sqm / (3 * math.sqrt(3)))
    
    # Convert meters to degrees
    lat_per_meter = 1.0 / 111000.0
    lon_per_meter = 1.0 / (111000.0 * math.cos(math.radians(center_lat)))
    
    # Radius of circumscribed circle equals side length for regular hexagon
    radius_m = side_length_m
    
    # Create 6 vertices (starting from top, going clockwise)
    coords = []
    for i in range(6):
        angle = math.radians(90 - 60 * i)  # Start at 90° (top), go clockwise
        lat = center_lat + radius_m * math.sin(angle) * lat_per_meter
        lon = center_lon + radius_m * math.cos(angle) * lon_per_meter
        coords.append((lon, lat))
    
    # Close the polygon
    coords.append(coords[0])
    
    return coords, side_length_m

# Create new KML document
kml_root = ET.Element('{http://www.opengis.net/kml/2.2}kml')
document = ET.SubElement(kml_root, '{http://www.opengis.net/kml/2.2}Document')

# Document name
doc_name = ET.SubElement(document, '{http://www.opengis.net/kml/2.2}name')
doc_name.text = "청라 신축 타워 448m (층별 면적 가변)"

# Create Folder for the building
folder = ET.SubElement(document, '{http://www.opengis.net/kml/2.2}Folder')
folder_name = ET.SubElement(folder, '{http://www.opengis.net/kml/2.2}name')
folder_name.text = "청라 신축 타워 (448m)"

print("\n" + "=" * 80)
print("층별 폴리곤 생성 중...")
print("=" * 80)

cumulative_height = 0.0

for floor_data in floors:
    floor_num = floor_data['floor']
    area = floor_data['area']
    
    # Calculate heights
    base_height = cumulative_height
    top_height = cumulative_height + floor_height
    cumulative_height = top_height
    
    # Create hexagon
    hex_coords, side_length = create_hexagon_from_area(CENTER_LAT, CENTER_LON, area)
    
    # Create Placemark
    placemark = ET.SubElement(folder, '{http://www.opengis.net/kml/2.2}Placemark')
    
    # Name
    name = ET.SubElement(placemark, '{http://www.opengis.net/kml/2.2}name')
    name.text = f"청라 신축 타워 - {floor_num}층"
    
    # Description
    desc = ET.SubElement(placemark, '{http://www.opengis.net/kml/2.2}description')
    desc.text = (f"층: {floor_num}\n"
                f"면적: {area:.2f}㎡\n"
                f"육각형 한 변: {side_length:.2f}m\n"
                f"높이: {base_height:.1f}m ~ {top_height:.1f}m")
    
    # Style
    style = ET.SubElement(placemark, '{http://www.opengis.net/kml/2.2}Style')
    
    # Line style (outline)
    line_style = ET.SubElement(style, '{http://www.opengis.net/kml/2.2}LineStyle')
    line_color = ET.SubElement(line_style, '{http://www.opengis.net/kml/2.2}color')
    line_color.text = 'ffffffff'  # White outline
    line_width = ET.SubElement(line_style, '{http://www.opengis.net/kml/2.2}width')
    line_width.text = '1.5'
    
    # Polygon style
    poly_style = ET.SubElement(style, '{http://www.opengis.net/kml/2.2}PolyStyle')
    poly_color = ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}color')
    # Gold color for super tall building (448m)
    poly_color.text = 'ff00d7ff'  # Opaque gold/yellow
    poly_fill = ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}fill')
    poly_fill.text = '1'
    poly_outline = ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}outline')
    poly_outline.text = '1'
    
    # Polygon geometry
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
    
    print(f"  {floor_num:>6}층: {area:>9.2f}㎡ (변={side_length:>5.1f}m) | {base_height:>6.1f}m ~ {top_height:>6.1f}m")

# Register namespace and save
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')
tree = ET.ElementTree(kml_root)
output_file = '청라신축타워_448m.kml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print("\n" + "=" * 80)
print("✓ 건물 생성 완료!")
print(f"  파일: {output_file}")
print(f"  위치: ({CENTER_LAT}, {CENTER_LON})")
print(f"  총 높이: {TOTAL_HEIGHT}m")
print(f"  층수: {total_floors}층")
print(f"  형태: 층별 면적에 따라 크기가 다른 육각형")
print(f"  색상: 골드 (448m 초고층 타워)")
print("=" * 80)

# Calculate statistics
areas = [f['area'] for f in floors]
print(f"\n면적 통계:")
print(f"  최소 면적: {min(areas):.2f}㎡")
print(f"  최대 면적: {max(areas):.2f}㎡")
print(f"  평균 면적: {sum(areas)/len(areas):.2f}㎡")
print("=" * 80)
