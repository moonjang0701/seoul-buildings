import xml.etree.ElementTree as ET
import math

# Perfect 파일 로드
tree = ET.parse('cheongna_buildings_5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# 청라시티타워 중심 좌표
CENTER_LON = 126.633973
CENTER_LAT = 37.533053
RADIUS_KM = 2.5

def haversine_distance(lon1, lat1, lon2, lat2):
    """두 좌표 간 거리 계산 (km)"""
    R = 6371  # 지구 반경 (km)
    
    # 라디안으로 변환
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    
    # Haversine 공식
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def get_building_center(coords_text):
    """건물 좌표의 중심점 계산"""
    import re
    coord_points = re.split(r'\s+', coords_text.strip())
    coord_points = [c.strip() for c in coord_points if c.strip()]
    
    if not coord_points:
        return None, None
    
    lons = []
    lats = []
    for coord in coord_points:
        parts = coord.split(',')
        if len(parts) >= 2:
            try:
                lons.append(float(parts[0]))
                lats.append(float(parts[1]))
            except ValueError:
                continue
    
    if not lons or not lats:
        return None, None
    
    # 중심점 (평균)
    center_lon = sum(lons) / len(lons)
    center_lat = sum(lats) / len(lats)
    
    return center_lon, center_lat

print(f"=== 반경 {RADIUS_KM}km 필터링 중... ===\n")
print(f"중심: ({CENTER_LON}, {CENTER_LAT})")

# 모든 Placemark 검사
placemarks = root.findall('.//kml:Placemark', ns)
total_buildings = len(placemarks)
print(f"총 건물: {total_buildings}개\n")

# 제거할 Placemark 찾기
to_remove = []
kept_buildings = []

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    name = name_elem.text if name_elem is not None else "Unknown"
    
    # 좌표 가져오기
    coords_elem = placemark.find('.//kml:coordinates', ns)
    if coords_elem is not None and coords_elem.text:
        center_lon, center_lat = get_building_center(coords_elem.text)
        
        if center_lon is not None and center_lat is not None:
            # 거리 계산
            distance = haversine_distance(CENTER_LON, CENTER_LAT, center_lon, center_lat)
            
            if distance <= RADIUS_KM:
                kept_buildings.append({
                    'name': name,
                    'distance': distance,
                    'coords': (center_lon, center_lat)
                })
            else:
                to_remove.append((placemark, name, distance))

print(f"필터 결과:")
print(f"  유지: {len(kept_buildings)}개")
print(f"  제거: {len(to_remove)}개")

# 제거할 Placemark 삭제
parent_map = {c: p for p in root.iter() for c in p}
for placemark, name, distance in to_remove:
    parent = parent_map.get(placemark)
    if parent is not None:
        parent.remove(placemark)

# Document 이름 변경
doc_name = root.find('.//kml:Document/kml:name', ns)
if doc_name is not None:
    doc_name.text = f'청라시티타워 반경 {RADIUS_KM}km 건물 (높이 1~299m)'

# 저장
output_file = f'cheongna_buildings_{RADIUS_KM}km_perfect.kml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"\n✅ 저장 완료: {output_file}")

# 파일 크기
import os
original_size = os.path.getsize('cheongna_buildings_5km_perfect.kml')
new_size = os.path.getsize(output_file)

print(f"\n파일 크기:")
print(f"  5km 버전: {original_size/1024/1024:.2f} MB")
print(f"  {RADIUS_KM}km 버전: {new_size/1024/1024:.2f} MB")
print(f"  감소: {((original_size-new_size)/original_size*100):.1f}%")

# 통계
print(f"\n=== 건물 통계 ===")
print(f"반경 {RADIUS_KM}km 이내 건물: {len(kept_buildings)}개")

# 가장 가까운/먼 건물
if kept_buildings:
    kept_buildings.sort(key=lambda x: x['distance'])
    print(f"\n가장 가까운 건물:")
    for i, b in enumerate(kept_buildings[:3], 1):
        print(f"  {i}. {b['name']} - {b['distance']:.2f}km")
    
    print(f"\n가장 먼 건물:")
    for i, b in enumerate(kept_buildings[-3:], 1):
        print(f"  {i}. {b['name']} - {b['distance']:.2f}km")
