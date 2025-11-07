#!/usr/bin/env python3
"""
Analyze 청라 디 이스트 buildings to identify properly modeled ones
"""
import xml.etree.ElementTree as ET
import re

# Parse KML
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

# Define namespace
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Find all placemarks
placemarks = root.findall('.//kml:Placemark', ns)

print("=" * 80)
print("청라 디 이스트 Buildings Analysis")
print("=" * 80)

dieast_buildings = []

for i, placemark in enumerate(placemarks):
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None and '청라 디 이스트' in name_elem.text:
        # Extract height from name
        height_match = re.search(r'\((\d+\.?\d*)m\)', name_elem.text)
        height = float(height_match.group(1)) if height_match else 0.0
        
        # Get coordinates
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
                
                # Calculate polygon "complexity" - distance from first to last point
                first_lon, first_lat = lons[0], lats[0]
                last_lon, last_lat = lons[-1], lats[-1]
                closure_distance = ((last_lon - first_lon)**2 + (last_lat - first_lat)**2)**0.5
                
                # Calculate bounding box dimensions
                width = max(lons) - min(lons)
                depth = max(lats) - min(lats)
                aspect_ratio = max(width, depth) / min(width, depth) if min(width, depth) > 0 else 0
                
                dieast_buildings.append({
                    'index': i,
                    'name': name_elem.text,
                    'height': height,
                    'center_lon': center_lon,
                    'center_lat': center_lat,
                    'num_points': len(coord_points),
                    'closure_distance': closure_distance,
                    'width': width * 111000,  # Convert to meters (approximate)
                    'depth': depth * 111000,  # Convert to meters (approximate)
                    'aspect_ratio': aspect_ratio
                })

print(f"\nFound {len(dieast_buildings)} buildings with '청라 디 이스트'\n")

# Sort by latitude (north to south)
dieast_buildings.sort(key=lambda x: x['center_lat'], reverse=True)

print("Buildings sorted by latitude (North to South):")
print("-" * 80)

for i, building in enumerate(dieast_buildings):
    print(f"\n{i+1}. {building['name']}")
    print(f"   Center: ({building['center_lat']:.6f}, {building['center_lon']:.6f})")
    print(f"   Coordinate points: {building['num_points']}")
    print(f"   Height: {building['height']}m")
    print(f"   Dimensions: {building['width']:.1f}m × {building['depth']:.1f}m")
    print(f"   Aspect ratio: {building['aspect_ratio']:.2f}")
    print(f"   Closure distance: {building['closure_distance']:.8f}")
    
    # Identify if it's a thin bar (high aspect ratio) or proper building
    if building['aspect_ratio'] > 5:
        print(f"   → THIN BAR (placeholder)")
    elif building['num_points'] > 10:
        print(f"   → WELL-MODELED building ✓")
    else:
        print(f"   → Simple polygon")

print("\n" + "=" * 80)
print("Analysis based on:")
print("- Thin bars: High aspect ratio (>5:1), few points")
print("- Well-modeled: Many points (>10), reasonable aspect ratio")
print("=" * 80)
