import xml.etree.ElementTree as ET
import re

# 원본 파일 분석
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}

placemarks = root.findall('.//kml:Placemark', ns)
print(f"총 건물 수: {len(placemarks)}\n")

# 문제 패턴 찾기
issues = []

for idx, placemark in enumerate(placemarks[:50]):  # 처음 50개 샘플
    name_elem = placemark.find('.//kml:name', ns)
    name = name_elem.text if name_elem is not None else f"Building_{idx}"
    
    # 모든 Polygon 찾기 (중복 여부 확인)
    polygons = placemark.findall('.//kml:Polygon', ns)
    
    if len(polygons) > 1:
        issues.append({
            'name': name,
            'type': 'multiple_polygons',
            'count': len(polygons),
            'detail': f'{len(polygons)}개 Polygon 중복'
        })
    
    # 좌표 분석
    for polygon in polygons:
        coords_elem = polygon.find('.//kml:coordinates', ns)
        if coords_elem:
            coords_text = coords_elem.text.strip()
            coord_points = re.split(r'\s+', coords_text)
            coord_points = [c for c in coord_points if c.strip()]
            
            # 중복 좌표 확인
            unique_coords = set(coord_points)
            if len(coord_points) != len(unique_coords) + 1:  # +1은 시작=끝 좌표
                issues.append({
                    'name': name,
                    'type': 'duplicate_coords',
                    'detail': f'총 {len(coord_points)}개 중 중복 있음'
                })
            
            # 동일 좌표 연속 확인
            for i in range(len(coord_points) - 1):
                if coord_points[i] == coord_points[i+1]:
                    issues.append({
                        'name': name,
                        'type': 'consecutive_same',
                        'detail': f'연속 동일 좌표: {coord_points[i]}'
                    })
                    break

print(f"발견된 문제: {len(issues)}개\n")

# 문제 유형별 통계
from collections import Counter
issue_types = Counter([i['type'] for i in issues])

print("=== 문제 유형 ===")
for itype, count in issue_types.items():
    print(f"  {itype}: {count}개")

print("\n=== 상세 (처음 10개) ===")
for i, issue in enumerate(issues[:10]):
    print(f"{i+1}. {issue['name']}")
    print(f"   유형: {issue['type']}")
    print(f"   상세: {issue['detail']}\n")

# LineString이나 MultiGeometry 확인
linestrings = root.findall('.//kml:LineString', ns)
multigeoms = root.findall('.//kml:MultiGeometry', ns)

print(f"=== 기하 요소 ===")
print(f"LineString: {len(linestrings)}개")
print(f"MultiGeometry: {len(multigeoms)}개")

if len(linestrings) > 0:
    print("⚠️ LineString이 있습니다! (선이 튀는 원인)")
if len(multigeoms) > 0:
    print("⚠️ MultiGeometry가 있습니다! (면 중복 원인)")
