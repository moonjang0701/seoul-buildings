#!/usr/bin/env python3
"""
Verify that only 라피아노 1단지 and 2단지 were restored
Confirm 청라푸르지오아파트 is NOT present
"""
import xml.etree.ElementTree as ET

# Parse KML
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
placemarks = root.findall('.//kml:Placemark', ns)

print("=" * 80)
print("Verification Report - 푸르지오 Buildings")
print("=" * 80)

# Count buildings
total_buildings = len(placemarks)
lapiano1_count = 0
lapiano2_count = 0
apartment_count = 0

lapiano1_buildings = []
lapiano2_buildings = []
apartment_buildings = []

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None:
        name = name_elem.text
        
        if '청라푸르지오라피아노 1단지' in name:
            lapiano1_count += 1
            lapiano1_buildings.append(name)
        elif '청라푸르지오라피아노 2단지' in name:
            lapiano2_count += 1
            lapiano2_buildings.append(name)
        elif '청라푸르지오아파트' in name and '더샵레이크파크' not in name:
            apartment_count += 1
            apartment_buildings.append(name)

print(f"\n📊 Building Statistics:")
print(f"   Total buildings: {total_buildings}")
print(f"\n   청라푸르지오라피아노 1단지: {lapiano1_count} buildings")
print(f"   청라푸르지오라피아노 2단지: {lapiano2_count} buildings")
print(f"   청라푸르지오아파트: {apartment_count} buildings")

print("\n" + "-" * 80)
print("✓ Restoration Verification:")
print("-" * 80)

if lapiano1_count > 0:
    print(f"✅ 청라푸르지오라피아노 1단지: {lapiano1_count} buildings restored")
else:
    print("⚠️  청라푸르지오라피아노 1단지: NOT FOUND")

if lapiano2_count > 0:
    print(f"✅ 청라푸르지오라피아노 2단지: {lapiano2_count} buildings restored")
else:
    print("⚠️  청라푸르지오라피아노 2단지: NOT FOUND")

print("\n" + "-" * 80)
print("✓ Exclusion Verification:")
print("-" * 80)

if apartment_count == 0:
    print("✅ 청라푸르지오아파트: Correctly excluded (0 buildings)")
else:
    print(f"⚠️  청라푸르지오아파트: {apartment_count} buildings found (should be 0)")
    for name in apartment_buildings:
        print(f"    - {name}")

print("\n" + "=" * 80)

if lapiano1_count > 0 and lapiano2_count > 0 and apartment_count == 0:
    print("✅ SUCCESS: Restoration completed correctly!")
    print(f"   • 라피아노 1단지: {lapiano1_count} buildings ✓")
    print(f"   • 라피아노 2단지: {lapiano2_count} buildings ✓")
    print(f"   • 푸르지오아파트: Excluded ✓")
else:
    print("⚠️  ISSUES DETECTED")

print("=" * 80)
