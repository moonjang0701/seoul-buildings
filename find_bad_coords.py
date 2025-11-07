import xml.etree.ElementTree as ET
import re

# KML 파일 파싱
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

# 네임스페이스
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

# 청라 지역 대략적인 범위 (인천 청라)
EXPECTED_LAT_MIN = 37.48
EXPECTED_LAT_MAX = 37.58
EXPECTED_LON_MIN = 126.6
EXPECTED_LON_MAX = 126.75

# 문제 좌표 찾기
placemarks = root.findall('.//kml:Placemark', ns)
print(f"총 Placemark 개수: {len(placemarks)}")
print("\n=== 이상한 좌표 검색 중... ===\n")

problematic_buildings = []

for idx, placemark in enumerate(placemarks):
    name_elem = placemark.find('.//kml:name', ns)
    name = name_elem.text if name_elem is not None else f"Building_{idx}"
    
    coords_elem = placemark.find('.//kml:coordinates', ns)
    if coords_elem is not None:
        coords_text = coords_elem.text.strip()
        coord_points = [c.strip() for c in coords_text.split() if c.strip()]
        
        has_problem = False
        problem_coords = []
        
        for coord in coord_points:
            parts = coord.split(',')
            if len(parts) >= 2:
                try:
                    lon = float(parts[0])
                    lat = float(parts[1])
                    
                    # 범위를 벗어나는 좌표 체크
                    if (lat < EXPECTED_LAT_MIN or lat > EXPECTED_LAT_MAX or
                        lon < EXPECTED_LON_MIN or lon > EXPECTED_LON_MAX):
                        has_problem = True
                        problem_coords.append(f"({lon}, {lat})")
                    
                    # 극단적인 값 체크 (지구 범위를 벗어남)
                    if abs(lat) > 90 or abs(lon) > 180:
                        has_problem = True
                        problem_coords.append(f"INVALID: ({lon}, {lat})")
                        
                except ValueError:
                    has_problem = True
                    problem_coords.append(f"PARSE_ERROR: {coord}")
        
        if has_problem:
            problematic_buildings.append({
                'name': name,
                'index': idx,
                'bad_coords': problem_coords,
                'total_coords': len(coord_points)
            })

print(f"발견된 문제 건물: {len(problematic_buildings)}개\n")

# 처음 20개만 출력
for i, building in enumerate(problematic_buildings[:20]):
    print(f"{i+1}. {building['name']} (인덱스: {building['index']})")
    print(f"   총 좌표: {building['total_coords']}개")
    print(f"   문제 좌표: {', '.join(building['bad_coords'][:5])}")
    if len(building['bad_coords']) > 5:
        print(f"   ... 외 {len(building['bad_coords'])-5}개 더")
    print()

if len(problematic_buildings) > 20:
    print(f"... 외 {len(problematic_buildings)-20}개 더\n")

# 통계
if problematic_buildings:
    print("=== 문제 유형 분석 ===")
    total_bad = len(problematic_buildings)
    print(f"전체 건물 중 {total_bad}개 ({total_bad/len(placemarks)*100:.1f}%)에 문제 있음")
