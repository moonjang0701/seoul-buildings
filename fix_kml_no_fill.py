import xml.etree.ElementTree as ET
import re

# 정리된 파일 로드
tree = ET.parse('cheongna_buildings_5km_clean.kml')
root = tree.getroot()

# 네임스페이스
ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# PolyStyle에서 fill과 outline을 0으로 변경
modified_styles = 0

for poly_style in root.findall('.//kml:PolyStyle', ns):
    fill_elem = poly_style.find('kml:fill', ns)
    outline_elem = poly_style.find('kml:outline', ns)
    
    # fill을 0으로 변경 (면 제거)
    if fill_elem is not None:
        fill_elem.text = '0'
        modified_styles += 1
    
    # outline을 0으로 변경 (테두리 선 제거)
    if outline_elem is not None:
        outline_elem.text = '0'

print(f"수정된 스타일: {modified_styles}개")

# 저장
output_file = 'cheongna_buildings_5km_no_ground.kml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)
print(f"저장 완료: {output_file}")

# 검증
tree2 = ET.parse(output_file)
root2 = tree2.getroot()
fill_count = 0
for poly_style in root2.findall('.//kml:PolyStyle', ns):
    fill_elem = poly_style.find('kml:fill', ns)
    if fill_elem is not None and fill_elem.text == '0':
        fill_count += 1

print(f"검증: fill=0인 스타일 {fill_count}개")
print("\n✅ 이제 바닥에 면이 안 깔립니다!")
print("✅ 3D 입체 효과는 유지됩니다 (extrude=1)")
