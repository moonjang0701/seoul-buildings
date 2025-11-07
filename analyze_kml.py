import xml.etree.ElementTree as ET
import re

# KML 파일 파싱
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

# 네임스페이스 추출
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# Placemark 찾기
placemarks = root.findall('.//kml:Placemark', ns)
print(f"총 Placemark 개수: {len(placemarks)}")

# 각 Placemark 분석
polygon_count = 0
polygon_with_extrude = 0
total_coords = 0
max_coords = 0
min_coords = float('inf')

for placemark in placemarks[:10]:  # 처음 10개만 샘플링
    name_elem = placemark.find('.//kml:name', ns)
    name = name_elem.text if name_elem is not None else "No name"
    
    polygon = placemark.find('.//kml:Polygon', ns)
    if polygon is not None:
        polygon_count += 1
        
        # extrude 확인
        extrude = polygon.find('.//kml:extrude', ns)
        if extrude is not None and extrude.text == '1':
            polygon_with_extrude += 1
        
        # 좌표 개수 확인
        coords_elem = polygon.find('.//kml:coordinates', ns)
        if coords_elem is not None:
            coords_text = coords_elem.text.strip()
            coord_points = [c.strip() for c in coords_text.split() if c.strip()]
            num_coords = len(coord_points)
            total_coords += num_coords
            max_coords = max(max_coords, num_coords)
            min_coords = min(min_coords, num_coords)
            
            print(f"\n건물: {name}")
            print(f"  좌표 개수: {num_coords}")
            print(f"  샘플 좌표: {coord_points[0] if coord_points else 'None'}")

print(f"\n=== 전체 분석 (샘플 10개) ===")
print(f"Polygon 개수: {polygon_count}")
print(f"Extrude=1인 Polygon: {polygon_with_extrude}")
print(f"평균 좌표 개수: {total_coords/polygon_count if polygon_count > 0 else 0:.2f}")
print(f"최대 좌표 개수: {max_coords}")
print(f"최소 좌표 개수: {min_coords}")
