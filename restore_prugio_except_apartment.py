#!/usr/bin/env python3
"""
Restore 청라푸르지오라피아노 1단지 and 2단지 buildings
Exclude 청라푸르지오아파트
"""
import xml.etree.ElementTree as ET
import math

# Parse both files
print("=" * 80)
print("Restoring 푸르지오 Buildings (except 아파트)")
print("=" * 80)

# Parse source file (5km with all buildings)
source_tree = ET.parse('cheongna_buildings_5km_perfect.kml')
source_root = source_tree.getroot()

# Parse target file (current 2.5km file)
target_tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
target_root = target_tree.getroot()

# Register namespace
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Get source and target documents
source_document = source_root.find('.//kml:Document', ns)
source_placemarks = source_root.findall('.//kml:Placemark', ns)

target_document = target_root.find('.//kml:Document', ns)

# Center point for 2.5km radius check
CENTER_LAT = 37.540134
CENTER_LON = 126.643091
RADIUS_KM = 2.5

def haversine_distance(lon1, lat1, lon2, lat2):
    """Calculate distance between two points in km"""
    R = 6371  # Earth radius in km
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_building_center(placemark):
    """Get center coordinates of a building"""
    coordinates_elem = placemark.find('.//kml:coordinates', ns)
    if coordinates_elem is not None:
        coord_text = coordinates_elem.text.strip()
        coord_points = [c.strip() for c in coord_text.split() if c.strip()]
        
        lons = []
        lats = []
        for coord in coord_points:
            parts = coord.split(',')
            if len(parts) >= 2:
                try:
                    lons.append(float(parts[0]))
                    lats.append(float(parts[1]))
                except:
                    continue
        
        if lons and lats:
            return sum(lats) / len(lats), sum(lons) / len(lons)
    return None, None

# Find prugio buildings to restore
buildings_to_restore = []

print("\n[1] Searching for 푸르지오 buildings in source file...")

for placemark in source_placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None:
        name = name_elem.text
        
        # Only restore 라피아노 1단지 and 2단지
        if '청라푸르지오라피아노' in name and ('1단지' in name or '2단지' in name):
            # Check if within 2.5km radius
            center_lat, center_lon = get_building_center(placemark)
            if center_lat and center_lon:
                distance = haversine_distance(CENTER_LON, CENTER_LAT, center_lon, center_lat)
                if distance <= RADIUS_KM:
                    buildings_to_restore.append((name, placemark))

print(f"   Found {len(buildings_to_restore)} buildings to restore")

# Count by type
lapiano1_count = sum(1 for name, _ in buildings_to_restore if '1단지' in name)
lapiano2_count = sum(1 for name, _ in buildings_to_restore if '2단지' in name)

print(f"   - 청라푸르지오라피아노 1단지: {lapiano1_count} buildings")
print(f"   - 청라푸르지오라피아노 2단지: {lapiano2_count} buildings")

# Add buildings to target document
print("\n[2] Adding buildings to target file...")

import copy
for name, placemark in buildings_to_restore:
    new_placemark = copy.deepcopy(placemark)
    target_document.append(new_placemark)

# Save
target_tree.write('cheongna_buildings_2.5km_perfect.kml', encoding='utf-8', xml_declaration=True)

print(f"\n✓ Restored {len(buildings_to_restore)} buildings")
print(f"✓ File saved: cheongna_buildings_2.5km_perfect.kml")

print("\n" + "=" * 80)
print("✓ Restoration completed!")
print("  Restored: 라피아노 1단지, 2단지")
print("  Excluded: 청라푸르지오아파트")
print("=" * 80)
