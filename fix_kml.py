import xml.etree.ElementTree as ET

# KML 파일 파싱
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

# 네임스페이스
ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# 모든 extrude 요소 찾아서 제거
removed_count = 0
for polygon in root.findall('.//kml:Polygon', ns):
    extrude = polygon.find('kml:extrude', ns)
    if extrude is not None:
        polygon.remove(extrude)
        removed_count += 1

print(f"제거된 extrude 개수: {removed_count}")

# 저장
tree.write('cheongna_buildings_5km_fixed.kml', encoding='utf-8', xml_declaration=True)
print("수정된 파일 저장 완료: cheongna_buildings_5km_fixed.kml")

# 파일 크기 비교
import os
original_size = os.path.getsize('cheongna_buildings_5km.kml')
fixed_size = os.path.getsize('cheongna_buildings_5km_fixed.kml')
print(f"\n원본 파일 크기: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
print(f"수정 파일 크기: {fixed_size:,} bytes ({fixed_size/1024/1024:.2f} MB)")
print(f"감소량: {original_size-fixed_size:,} bytes ({(1-fixed_size/original_size)*100:.1f}% 감소)")
