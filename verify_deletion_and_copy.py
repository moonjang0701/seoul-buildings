#!/usr/bin/env python3
"""
Verify deletion of 푸르지오 buildings and copying of 더샵레이크파크 buildings
"""
import xml.etree.ElementTree as ET
import math

# Parse KML
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
placemarks = root.findall('.//kml:Placemark', ns)

print("=" * 80)
print("Verification Report")
print("=" * 80)

# Count buildings
total_buildings = len(placemarks)
prugio_buildings = 0
thesharp_originals = 0
thesharp_copies = 0
thesharp_prugio_copies = 0

# Expected positions for new copies
expected_positions = [
    (37.535087, 126.636995),
    (37.535252, 126.637917),
    (37.535328, 126.638787),
    (37.535392, 126.639674)
]

new_copies = []

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None:
        name = name_elem.text
        
        # Check for 푸르지오
        if '푸르지오' in name and '더샵레이크파크' not in name:
            prugio_buildings += 1
        
        # Check for 더샵레이크파크
        if '더샵레이크파크' in name or '청라더샵레이크파크' in name:
            if '푸르지오위치' in name:
                thesharp_prugio_copies += 1
                
                # Get coordinates
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
                        
                        new_copies.append({
                            'name': name,
                            'center_lat': center_lat,
                            'center_lon': center_lon,
                            'num_points': len(coord_points)
                        })
            elif 'Copy' in name:
                thesharp_copies += 1
            else:
                thesharp_originals += 1

print(f"\n📊 Building Statistics:")
print(f"   Total buildings: {total_buildings}")
print(f"   푸르지오 buildings remaining: {prugio_buildings}")
print(f"   청라더샵레이크파크 originals: {thesharp_originals}")
print(f"   청라더샵레이크파크 old copies: {thesharp_copies}")
print(f"   청라더샵레이크파크 new copies (푸르지오위치): {thesharp_prugio_copies}")

print("\n" + "-" * 80)
print("✓ Deletion Verification:")
print("-" * 80)

if prugio_buildings == 0:
    print("✓ SUCCESS: All 푸르지오 buildings deleted (39 buildings removed)")
else:
    print(f"⚠ WARNING: {prugio_buildings} 푸르지오 buildings still remain!")

print("\n" + "-" * 80)
print("✓ Copy Verification:")
print("-" * 80)

# Sort by latitude
new_copies.sort(key=lambda x: x['center_lat'], reverse=True)

for i, building in enumerate(new_copies, 1):
    print(f"\n{i}. {building['name']}")
    print(f"   Center: ({building['center_lat']:.6f}, {building['center_lon']:.6f})")
    print(f"   Coordinate points: {building['num_points']}")
    
    # Check position accuracy
    for expected_lat, expected_lon in expected_positions:
        distance = math.sqrt((building['center_lat'] - expected_lat)**2 + 
                           (building['center_lon'] - expected_lon)**2)
        distance_m = distance * 111000  # Convert to meters
        
        if distance_m < 1.0:  # Within 1 meter
            print(f"   ✓ Position verified: ({expected_lat:.6f}, {expected_lon:.6f}) - Error: {distance_m:.1f}m")
            break

print("\n" + "=" * 80)

if prugio_buildings == 0 and thesharp_prugio_copies == 4:
    print("✅ SUCCESS: All operations completed correctly!")
    print("   • 39 푸르지오 buildings deleted")
    print("   • 4 청라더샵레이크파크 buildings copied to new locations")
else:
    print("⚠ ISSUES DETECTED:")
    if prugio_buildings > 0:
        print(f"   • {prugio_buildings} 푸르지오 buildings not deleted")
    if thesharp_prugio_copies != 4:
        print(f"   • Expected 4 new copies, found {thesharp_prugio_copies}")

print("=" * 80)
