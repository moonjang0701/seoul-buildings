#!/usr/bin/env python3
"""
Copy 청라 디 이스트 buildings to specified locations
- Copy bottom-right building (37.526670, 126.623173) to 1 location
- Copy middle-left building (37.527734, 126.624203) to 7 locations
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
print("Copying 청라 디 이스트 Buildings")
print("=" * 80)

def find_building_by_center(target_lat, target_lon, tolerance=0.0001):
    """Find building by its center coordinates"""
    for placemark in placemarks:
        name_elem = placemark.find('.//kml:name', ns)
        if name_elem is not None and '청라 디 이스트' in name_elem.text:
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
                    
                    # Check if this is the target building
                    if abs(center_lat - target_lat) < tolerance and abs(center_lon - target_lon) < tolerance:
                        return placemark, center_lat, center_lon, name_elem.text
    return None, None, None, None

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
    
    print(f"✓ Copied to ({target_lat:.6f}, {target_lon:.6f}) - {copy_name}")
    return new_placemark

# ============================================================================
# STEP 1: Copy BOTTOM-RIGHT building (37.526670, 126.623173) to 1 location
# ============================================================================
print("\n[1] Finding BOTTOM-RIGHT building (37.526670, 126.623173)...")
source1, center1_lat, center1_lon, name1 = find_building_by_center(37.526670, 126.623173)

if source1:
    print(f"    Found: {name1}")
    print(f"    Center: ({center1_lat:.6f}, {center1_lon:.6f})")
    
    # Copy to 1 location
    target1 = (37.527302, 126.622974)
    print(f"\n    Copying to 1 location:")
    copy_building_to_location(source1, center1_lat, center1_lon, name1, 
                             target1[0], target1[1], "Copy-1")
else:
    print("    ERROR: Building not found!")

# ============================================================================
# STEP 2: Copy MIDDLE-LEFT building (37.527734, 126.624203) to 7 locations
# ============================================================================
print("\n[2] Finding MIDDLE-LEFT building (37.527734, 126.624203)...")
source2, center2_lat, center2_lon, name2 = find_building_by_center(37.527734, 126.624203)

if source2:
    print(f"    Found: {name2}")
    print(f"    Center: ({center2_lat:.6f}, {center2_lon:.6f})")
    
    # Copy to 7 locations
    targets = [
        (37.526918, 126.624515),
        (37.525738, 126.623513),
        (37.526073, 126.624895),
        (37.524977, 126.623893),
        (37.525326, 126.625191),
        (37.524414, 126.624130),
        (37.524786, 126.625445)
    ]
    
    print(f"\n    Copying to {len(targets)} locations:")
    for i, (target_lat, target_lon) in enumerate(targets, 1):
        copy_building_to_location(source2, center2_lat, center2_lon, name2,
                                 target_lat, target_lon, f"Copy-{i}")
else:
    print("    ERROR: Building not found!")

# Save the updated KML
tree.write('cheongna_buildings_2.5km_perfect.kml', encoding='utf-8', xml_declaration=True)

print("\n" + "=" * 80)
print("✓ Successfully copied buildings!")
print(f"✓ File saved: cheongna_buildings_2.5km_perfect.kml")
print("=" * 80)
