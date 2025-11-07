import xml.etree.ElementTree as ET

# 정리된 파일 로드
tree = ET.parse('cheongna_buildings_5km_clean.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

print("=== KML 색상 옵션 생성 ===\n")

# 옵션 1: fill=0, outline=0 (이미 생성됨)
print("✅ 옵션 1: cheongna_buildings_5km_no_ground.kml")
print("   - fill=0, outline=0")
print("   - 바닥 면 없음, 테두리 없음")
print("   - 깜빡임 완전 제거")
print("   - 3D 건물 벽면만 (색상 없음)")

# 옵션 2: fill=0, outline=1, 단색 LineStyle
tree2 = ET.parse('cheongna_buildings_5km_clean.kml')
root2 = tree2.getroot()

# LineStyle만 활성화, PolyStyle은 비활성화
for poly_style in root2.findall('.//kml:PolyStyle', ns):
    fill_elem = poly_style.find('kml:fill', ns)
    outline_elem = poly_style.find('kml:outline', ns)
    
    if fill_elem is not None:
        fill_elem.text = '0'  # 면 제거
    if outline_elem is not None:
        outline_elem.text = '1'  # 테두리만 유지

# LineStyle 색상 조정 (더 선명하게)
for line_style in root2.findall('.//kml:LineStyle', ns):
    width_elem = line_style.find('kml:width', ns)
    if width_elem is not None:
        width_elem.text = '2'  # 선 두께 증가

tree2.write('cheongna_buildings_5km_outline_only.kml', encoding='utf-8', xml_declaration=True)
print("\n✅ 옵션 2: cheongna_buildings_5km_outline_only.kml")
print("   - fill=0, outline=1")
print("   - 바닥 면 없음, 테두리만 있음")
print("   - 건물 색상으로 테두리 표시")
print("   - 깜빡임 감소")

print("\n=== 추천 ===")
print("깜빡임이 심하다면: 옵션 1 (no_ground) 사용")
print("색상을 보고 싶다면: 옵션 2 (outline_only) 사용")

import os
print(f"\n파일 크기:")
print(f"  no_ground: {os.path.getsize('cheongna_buildings_5km_no_ground.kml')/1024/1024:.2f} MB")
print(f"  outline_only: {os.path.getsize('cheongna_buildings_5km_outline_only.kml')/1024/1024:.2f} MB")
