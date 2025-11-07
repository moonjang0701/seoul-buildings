import xml.etree.ElementTree as ET
import re

# 파일 로드
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# 청라더샵레이크파크 관련 건물 찾기
placemarks = root.findall('.//kml:Placemark', ns)
lake_park_buildings = []

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None and '청라더샵레이크파크' in name_elem.text:
        # 좌표 중심점 계산
        coords_elem = placemark.find('.//kml:coordinates', ns)
        if coords_elem is not None:
            coords_text = coords_elem.text.strip()
            coord_points = re.split(r'\s+', coords_text)
            coord_points = [c.strip() for c in coord_points if c.strip()]
            
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
                
                lake_park_buildings.append({
                    'name': name_elem.text,
                    'center': (center_lat, center_lon),
                    'coords_count': len(coord_points)
                })

print("=== 청라더샵레이크파크 건물 목록 ===\n")
for i, building in enumerate(lake_park_buildings, 1):
    print(f"{i}. {building['name']}")
    print(f"   중심: ({building['center'][0]:.7f}, {building['center'][1]:.7f})")
    print(f"   좌표 개수: {building['coords_count']}개")
    print()

print(f"총 {len(lake_park_buildings)}개 건물")

# 요청한 위치와 비교
requested = [
    (37.530835, 126.638879, "Copy 1"),
    (37.53083906814747, 126.63797714584872, "Copy 2"),
    (37.530824759044826, 126.63702985257429, "Copy 3")
]

print("\n=== 위치 검증 ===\n")
for req_lat, req_lon, name in requested:
    # 가장 가까운 건물 찾기
    min_dist = float('inf')
    closest = None
    
    for building in lake_park_buildings:
        lat, lon = building['center']
        dist = ((lat - req_lat)**2 + (lon - req_lon)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest = building
    
    if closest and min_dist < 0.0001:  # 약 10m 이내
        print(f"✅ {name}: {closest['name']}")
        print(f"   요청: ({req_lat:.7f}, {req_lon:.7f})")
        print(f"   실제: ({closest['center'][0]:.7f}, {closest['center'][1]:.7f})")
        print(f"   오차: {min_dist*111000:.1f}m")
    else:
        print(f"❌ {name}: 위치 불일치")
    print()
