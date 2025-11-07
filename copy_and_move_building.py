import xml.etree.ElementTree as ET
import re
import copy

# 2.5km 파일 로드
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# 청라더샵레이크파크 찾기
placemarks = root.findall('.//kml:Placemark', ns)
document = root.find('.//kml:Document', ns)
lake_park = None

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None and '청라더샵레이크파크' in name_elem.text:
        lake_park = placemark
        break

if lake_park is None:
    print("❌ 청라더샵레이크파크를 찾을 수 없습니다.")
    exit(1)

# 원본 좌표 가져오기 및 중심점 계산
coords_elem = lake_park.find('.//kml:coordinates', ns)
coords_text = coords_elem.text.strip()
coord_points = re.split(r'\s+', coords_text)
coord_points = [c.strip() for c in coord_points if c.strip()]

# 원본 중심점 계산
lons = []
lats = []
heights = []

for coord in coord_points:
    parts = coord.split(',')
    if len(parts) >= 2:
        lons.append(float(parts[0]))
        lats.append(float(parts[1]))
        if len(parts) >= 3:
            heights.append(float(parts[2]))

original_center_lon = sum(lons) / len(lons)
original_center_lat = sum(lats) / len(lats)
print(f"원본 중심: ({original_center_lon:.6f}, {original_center_lat:.6f})")

# 새 위치 (중심 좌표)
new_locations = [
    (37.530835, 126.638879, "Copy 1"),
    (37.53083906814747, 126.63797714584872, "Copy 2"),
    (37.530824759044826, 126.63702985257429, "Copy 3")
]

# 각 위치에 대해 복사 및 이동
for new_lat, new_lon, copy_name in new_locations:
    # Placemark 복사
    new_placemark = copy.deepcopy(lake_park)
    
    # 이름 변경
    name_elem = new_placemark.find('.//kml:name', ns)
    if name_elem is not None:
        original_name = name_elem.text
        name_elem.text = f"{original_name} - {copy_name}"
    
    # 좌표 이동
    new_coords_elem = new_placemark.find('.//kml:coordinates', ns)
    if new_coords_elem is not None:
        # 오프셋 계산 (새 중심 - 원본 중심)
        offset_lon = new_lon - original_center_lon
        offset_lat = new_lat - original_center_lat
        
        # 모든 좌표에 오프셋 적용
        new_coords = []
        for coord in coord_points:
            parts = coord.split(',')
            if len(parts) >= 2:
                old_lon = float(parts[0])
                old_lat = float(parts[1])
                new_coord_lon = old_lon + offset_lon
                new_coord_lat = old_lat + offset_lat
                
                if len(parts) >= 3:
                    height = parts[2]
                    new_coords.append(f"{new_coord_lon:.7f},{new_coord_lat:.7f},{height}")
                else:
                    new_coords.append(f"{new_coord_lon:.7f},{new_coord_lat:.7f}")
        
        # 새 좌표 적용 (줄바꿈 형식)
        new_coords_elem.text = '\n              ' + '\n              '.join(new_coords) + '\n            '
    
    # Document에 추가
    if document is not None:
        document.append(new_placemark)
        print(f"✅ 추가됨: {name_elem.text} at ({new_lat:.6f}, {new_lon:.6f})")

# 저장
tree.write('cheongna_buildings_2.5km_perfect.kml', encoding='utf-8', xml_declaration=True)

print(f"\n✅ 완료! 3개의 건물이 추가되었습니다.")
print(f"총 건물 수: {len(placemarks)} → {len(placemarks) + 3}")

# 파일 크기
import os
file_size = os.path.getsize('cheongna_buildings_2.5km_perfect.kml')
print(f"파일 크기: {file_size/1024/1024:.2f} MB")
