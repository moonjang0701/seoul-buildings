import xml.etree.ElementTree as ET

# 정리된 파일 로드
tree = ET.parse('cheongna_buildings_5km_clean.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

print("=== 입체감 있는 3D 건물 생성 ===\n")

# 옵션 1: fill=1, outline=0 (면만, 선 없음)
# 이렇게 하면 벽면은 채워지고 바닥 깜빡임도 줄어듦
for poly_style in root.findall('.//kml:PolyStyle', ns):
    fill_elem = poly_style.find('kml:fill', ns)
    outline_elem = poly_style.find('kml:outline', ns)
    
    if fill_elem is not None:
        fill_elem.text = '1'  # 면 활성화
    if outline_elem is not None:
        outline_elem.text = '0'  # 선 비활성화

# 색상 불투명도 조정 (더 진하게)
for poly_style in root.findall('.//kml:PolyStyle', ns):
    color_elem = poly_style.find('kml:color', ns)
    if color_elem is not None:
        color = color_elem.text
        # KML 색상 형식: aabbggrr (aa=alpha/투명도)
        # 7f (50% 투명) → cc (80% 불투명)로 변경
        if color.startswith('7f'):
            color_elem.text = 'cc' + color[2:]
            print(f"색상 조정: {color} → {color_elem.text}")

output_file = 'cheongna_buildings_5km_solid.kml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"\n✅ 생성 완료: {output_file}")
print("\n특징:")
print("  • fill=1, outline=0")
print("  • 벽면 채워짐 (입체감 UP)")
print("  • 테두리 선 없음 (깜빡임 감소)")
print("  • 색상 80% 불투명 (더 진하게)")
print("  • 바닥면도 보일 수 있음 (trade-off)")

import os
print(f"\n파일 크기: {os.path.getsize(output_file)/1024/1024:.2f} MB")
