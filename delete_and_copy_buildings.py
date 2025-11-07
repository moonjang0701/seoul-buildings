#!/usr/bin/env python3
"""
1. Delete all 청라푸르지오 buildings
2. Copy 청라더샵레이크파크 buildings to 4 new locations
"""
import xml.etree.ElementTree as ET
import copy

# Parse KML
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

# Register namespace
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Find document element
document = root.find('.//kml:Document', ns)
placemarks = root.findall('.//kml:Placemark', ns)

print("=" * 80)
print("Building Deletion and Copy Operation")
print("=" * 80)

# ============================================================================
# STEP 1: Delete all 청라푸르지오 buildings
# ============================================================================
print("\n[STEP 1] Deleting 청라푸르지오 buildings...")

deleted_count = 0
placemarks_to_delete = []

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None and '푸르지오' in name_elem.text:
        placemarks_to_delete.append(placemark)
        deleted_count += 1

# Delete the placemarks
for placemark in placemarks_to_delete:
    document.remove(placemark)

print(f"✓ Deleted {deleted_count} 푸르지오 buildings")

# ============================================================================
# STEP 2: Find 청라더샵레이크파크 original building
# ============================================================================
print("\n[STEP 2] Finding 청라더샵레이크파크 original building...")

# Refresh placemarks list after deletion
placemarks = root.findall('.//kml:Placemark', ns)

source_building = None
source_center_lat = None
source_center_lon = None
source_name = None

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None and '청라더샵레이크파크' in name_elem.text and 'Copy' not in name_elem.text:
        # Get coordinates to calculate center
        coordinates_elem = placemark.find('.//kml:coordinates', ns)
        if coordinates_elem is not None:
            coord_text = coordinates_elem.text.strip()
            coord_points = [c.strip() for c in coord_text.split() if c.strip()]
            
            # Calculate center
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
                
                # Use the first original building found
                source_building = placemark
                source_center_lat = center_lat
                source_center_lon = center_lon
                source_name = name_elem.text
                break

if source_building is not None:
    print(f"✓ Found: {source_name}")
    print(f"  Center: ({source_center_lat:.6f}, {source_center_lon:.6f})")
    
    # Count coordinate points
    coordinates_elem = source_building.find('.//kml:coordinates', ns)
    coord_text = coordinates_elem.text.strip()
    coord_points = [c.strip() for c in coord_text.split() if c.strip()]
    print(f"  Coordinate points: {len(coord_points)}")
else:
    print("✗ ERROR: 청라더샵레이크파크 building not found!")
    exit(1)

# ============================================================================
# STEP 3: Copy building to 4 new locations
# ============================================================================
print("\n[STEP 3] Copying 청라더샵레이크파크 to 4 new locations...")

target_locations = [
    (37.535087, 126.636995),
    (37.535252, 126.637917),
    (37.535328, 126.638787),
    (37.535392, 126.639674)
]

def copy_building_to_location(source_placemark, source_center_lat, source_center_lon, 
                              source_name, target_lat, target_lon, copy_name):
    """Copy a building and move it to a new location"""
    # Deep copy the placemark
    new_placemark = copy.deepcopy(source_placemark)
    
    # Update name
    name_elem = new_placemark.find('.//kml:name', ns)
    name_elem.text = f"{source_name} - {copy_name}"
    
    # Calculate offset
    offset_lon = target_lon - source_center_lon
    offset_lat = target_lat - source_center_lat
    
    # Update coordinates
    coordinates_elem = new_placemark.find('.//kml:coordinates', ns)
    coord_text = coordinates_elem.text.strip()
    coord_points = [c.strip() for c in coord_text.split() if c.strip()]
    
    new_coords = []
    for coord in coord_points:
        parts = coord.split(',')
        old_lon = float(parts[0])
        old_lat = float(parts[1])
        height = parts[2] if len(parts) > 2 else '0'
        
        new_lon = old_lon + offset_lon
        new_lat = old_lat + offset_lat
        
        new_coords.append(f"{new_lon:.7f},{new_lat:.7f},{height}")
    
    coordinates_elem.text = '\n' + ' '.join(new_coords) + '\n'
    
    # Add to document
    document.append(new_placemark)
    
    print(f"  ✓ Copied to ({target_lat:.6f}, {target_lon:.6f}) - {copy_name}")
    return new_placemark

# Copy to all locations
for i, (target_lat, target_lon) in enumerate(target_locations, 1):
    copy_building_to_location(source_building, source_center_lat, source_center_lon,
                             source_name, target_lat, target_lon, f"푸르지오위치-{i}")

# Save the updated KML
tree.write('cheongna_buildings_2.5km_perfect.kml', encoding='utf-8', xml_declaration=True)

print("\n" + "=" * 80)
print("✓ Operation completed successfully!")
print(f"✓ Deleted: {deleted_count} 푸르지오 buildings")
print(f"✓ Added: 4 청라더샵레이크파크 copies")
print(f"✓ File saved: cheongna_buildings_2.5km_perfect.kml")
print("=" * 80)
