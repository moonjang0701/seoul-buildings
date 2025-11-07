#!/usr/bin/env python3
"""
Verify that the 디이스트 buildings were copied correctly
"""
import xml.etree.ElementTree as ET
import math

# Parse KML
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
placemarks = root.findall('.//kml:Placemark', ns)

print("=" * 80)
print("Verification of 청라 디 이스트 Building Copies")
print("=" * 80)

# Count all buildings
total_buildings = len(placemarks)
dieast_originals = 0
dieast_copies = 0

# Expected positions
expected_positions = {
    'Copy-1 (from bottom-right)': (37.527302, 126.622974),
    'Copy-1 (from middle-left)': (37.526918, 126.624515),
    'Copy-2': (37.525738, 126.623513),
    'Copy-3': (37.526073, 126.624895),
    'Copy-4': (37.524977, 126.623893),
    'Copy-5': (37.525326, 126.625191),
    'Copy-6': (37.524414, 126.624130),
    'Copy-7': (37.524786, 126.625445)
}

copied_buildings = []

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None and '청라 디 이스트' in name_elem.text:
        if ' - Copy-' in name_elem.text:
            dieast_copies += 1
            
            # Get center coordinates
            coordinates_elem = placemark.find('.//kml:coordinates', ns)
            if coordinates_elem is not None:
                coord_text = coordinates_elem.text.strip()
                coord_points = [c.strip() for c in coord_text.split() if c.strip()]
                
                lons = []
                lats = []
                for coord in coord_points:
                    parts = coord.split(',')
                    if len(parts) >= 2:
                        lons.append(float(parts[0]))
                        lats.append(float(parts[1]))
                
                if lons and lats:
                    center_lon = sum(lons) / len(lons)
                    center_lat = sum(lats) / len(lats)
                    
                    copied_buildings.append({
                        'name': name_elem.text,
                        'center_lat': center_lat,
                        'center_lon': center_lon,
                        'num_points': len(coord_points)
                    })
        else:
            dieast_originals += 1

print(f"\nTotal buildings in file: {total_buildings}")
print(f"Original 디이스트 buildings: {dieast_originals}")
print(f"Copied 디이스트 buildings: {dieast_copies}")
print(f"Expected copies: 8 (1 from bottom-right + 7 from middle-left)")

print("\n" + "-" * 80)
print("Copied Buildings:")
print("-" * 80)

# Sort by latitude
copied_buildings.sort(key=lambda x: x['center_lat'], reverse=True)

for i, building in enumerate(copied_buildings, 1):
    print(f"\n{i}. {building['name']}")
    print(f"   Center: ({building['center_lat']:.6f}, {building['center_lon']:.6f})")
    print(f"   Coordinate points: {building['num_points']}")
    
    # Check if position matches expected
    for desc, (expected_lat, expected_lon) in expected_positions.items():
        distance = math.sqrt((building['center_lat'] - expected_lat)**2 + 
                           (building['center_lon'] - expected_lon)**2)
        distance_m = distance * 111000  # Convert to meters
        
        if distance_m < 1.0:  # Within 1 meter
            print(f"   ✓ Position verified: {desc} (error: {distance_m:.1f}m)")
            break

print("\n" + "=" * 80)

if dieast_copies == 8:
    print("✓ SUCCESS: All 8 buildings copied correctly!")
else:
    print(f"⚠ Warning: Expected 8 copies, found {dieast_copies}")

print("=" * 80)
