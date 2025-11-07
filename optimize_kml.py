import xml.etree.ElementTree as ET
import re

# KML 파일 파싱
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

# 네임스페이스
ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# 좌표 정밀도 줄이는 함수
def round_coordinate(coord_str, decimal_places=6):
    """좌표 정밀도를 줄임 (소수점 6자리면 약 10cm 정확도)"""
    parts = coord_str.split(',')
    if len(parts) >= 2:
        lon = round(float(parts[0]), decimal_places)
        lat = round(float(parts[1]), decimal_places)
        if len(parts) == 3:
            # 높이는 소수점 1자리로
            height = round(float(parts[2]), 1)
            return f"{lon},{lat},{height}"
        return f"{lon},{lat}"
    return coord_str

# 모든 Polygon 처리
removed_extrude = 0
optimized_coords = 0

for polygon in root.findall('.//kml:Polygon', ns):
    # extrude 제거
    extrude = polygon.find('kml:extrude', ns)
    if extrude is not None:
        polygon.remove(extrude)
        removed_extrude += 1
    
    # 좌표 최적화
    coords_elem = polygon.find('.//kml:coordinates', ns)
    if coords_elem is not None:
        coords_text = coords_elem.text.strip()
        coord_points = [c.strip() for c in coords_text.split() if c.strip()]
        
        # 각 좌표 정밀도 줄이기
        optimized_points = [round_coordinate(c) for c in coord_points]
        
        # 공백으로 구분하여 다시 저장 (줄바꿈 제거로 더 간결하게)
        coords_elem.text = ' '.join(optimized_points)
        optimized_coords += 1

print(f"제거된 extrude: {removed_extrude}개")
print(f"최적화된 좌표: {optimized_coords}개")

# 저장
tree.write('cheongna_buildings_5km_optimized.kml', encoding='utf-8', xml_declaration=True)
print("최적화 파일 저장 완료: cheongna_buildings_5km_optimized.kml")

# 파일 크기 비교
import os
original_size = os.path.getsize('cheongna_buildings_5km.kml')
optimized_size = os.path.getsize('cheongna_buildings_5km_optimized.kml')
print(f"\n원본 파일: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
print(f"최적화 파일: {optimized_size:,} bytes ({optimized_size/1024/1024:.2f} MB)")
print(f"감소량: {original_size-optimized_size:,} bytes ({(1-optimized_size/original_size)*100:.1f}% 감소)")
