import xml.etree.ElementTree as ET
import re

# KML 파일 파싱
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

# 네임스페이스
ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# 좌표 정규화 함수
def normalize_coordinate(coord_str, decimal_places=7):
    """좌표를 정규화하고 유효성 검사"""
    parts = coord_str.split(',')
    if len(parts) >= 2:
        try:
            lon = float(parts[0])
            lat = float(parts[1])
            
            # 유효성 검사
            if abs(lat) > 90 or abs(lon) > 180:
                return None
            
            # 정밀도 조정
            lon = round(lon, decimal_places)
            lat = round(lat, decimal_places)
            
            if len(parts) >= 3:
                height = round(float(parts[2]), 1)
                return f"{lon},{lat},{height}"
            return f"{lon},{lat}"
        except (ValueError, IndexError):
            return None
    return None

# 통계
fixed_count = 0
removed_count = 0
error_count = 0

# 모든 Placemark 처리
placemarks_to_remove = []

for placemark in root.findall('.//kml:Placemark', ns):
    name_elem = placemark.find('.//kml:name', ns)
    name = name_elem.text if name_elem is not None else "Unknown"
    
    # Polygon의 좌표 처리
    for coords_elem in placemark.findall('.//kml:coordinates', ns):
        if coords_elem.text:
            coords_text = coords_elem.text.strip()
            
            # 모든 공백/줄바꿈으로 분리
            coord_points = re.split(r'\s+', coords_text)
            coord_points = [c.strip() for c in coord_points if c.strip()]
            
            # 각 좌표 정규화
            normalized_coords = []
            has_error = False
            
            for coord in coord_points:
                normalized = normalize_coordinate(coord)
                if normalized:
                    normalized_coords.append(normalized)
                else:
                    has_error = True
                    error_count += 1
            
            # 유효한 좌표가 3개 이상 있어야 Polygon 유지
            if len(normalized_coords) >= 3 and not has_error:
                # 표준 포맷으로 저장: 공백으로 구분
                coords_elem.text = ' '.join(normalized_coords)
                fixed_count += 1
            else:
                # 문제가 있는 Placemark는 제거 표시
                placemarks_to_remove.append((placemark, name))
                removed_count += 1

# 문제 있는 Placemark 제거
parent_map = {c: p for p in root.iter() for c in p}
for placemark, name in placemarks_to_remove:
    parent = parent_map.get(placemark)
    if parent is not None:
        parent.remove(placemark)
        print(f"제거됨: {name}")

print(f"\n=== 처리 완료 ===")
print(f"수정된 건물: {fixed_count}개")
print(f"제거된 건물: {removed_count}개")
print(f"오류 좌표: {error_count}개")

# 저장
output_file = 'cheongna_buildings_5km_clean.kml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)
print(f"\n정리된 파일 저장: {output_file}")

# 파일 크기 비교
import os
original_size = os.path.getsize('cheongna_buildings_5km.kml')
clean_size = os.path.getsize(output_file)
print(f"\n원본 파일: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
print(f"정리 파일: {clean_size:,} bytes ({clean_size/1024/1024:.2f} MB)")
print(f"변화: {((clean_size-original_size)/original_size*100):+.1f}%")
